from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import get_db
from models.trade import Trade
from models.user import User
from models.schemas import AnalyticsResponse
from auth.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/", response_model=AnalyticsResponse)
def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all trades for user
    trades = db.query(Trade).filter(Trade.user_id == current_user.user_id).all()
    
    # Get closed trades (have exit_price and exit_date)
    closed_trades = [t for t in trades if t.exit_price is not None and t.exit_date is not None]
    
    total_trades = len(trades)
    total_closed = len(closed_trades)
    
    if total_closed == 0:
        return AnalyticsResponse(
            total_trades=total_trades,
            closed_trades=0,
            win_rate=0.0,
            avg_rrr=0.0,
            total_pnl=0.0,
            profit_factor=0.0,
            winning_trades=0,
            losing_trades=0,
            total_profit=0.0,
            total_loss=0.0
        )
    
    # Calculate PnL for each closed trade
    winning_trades = []
    losing_trades = []
    rrr_list = []
    
    for trade in closed_trades:
        # Calculate PnL based on trade type
        if trade.trade_type == "BUY":
            pnl = (trade.exit_price - trade.entry_price) * trade.lot_quantity
        else:  # SELL
            pnl = (trade.entry_price - trade.exit_price) * trade.lot_quantity
        
        # Calculate Risk-Reward Ratio if stop_loss and target_price exist
        if trade.stop_loss and trade.target_price:
            if trade.trade_type == "BUY":
                risk = abs(trade.entry_price - trade.stop_loss) * trade.lot_quantity
                reward = abs(trade.target_price - trade.entry_price) * trade.lot_quantity
            else:  # SELL
                risk = abs(trade.stop_loss - trade.entry_price) * trade.lot_quantity
                reward = abs(trade.entry_price - trade.target_price) * trade.lot_quantity
            
            if risk > 0:
                rrr = reward / risk
                rrr_list.append(rrr)
        
        if pnl > 0:
            winning_trades.append(pnl)
        elif pnl < 0:
            losing_trades.append(abs(pnl))
    
    # Calculate metrics
    total_profit = sum(winning_trades)
    total_loss = sum(losing_trades)
    total_pnl = total_profit - total_loss
    
    win_count = len(winning_trades)
    loss_count = len(losing_trades)
    win_rate = (win_count / total_closed * 100) if total_closed > 0 else 0.0
    
    avg_rrr = sum(rrr_list) / len(rrr_list) if rrr_list else 0.0
    profit_factor = (total_profit / total_loss) if total_loss > 0 else (total_profit if total_profit > 0 else 0.0)
    
    return AnalyticsResponse(
        total_trades=total_trades,
        closed_trades=total_closed,
        win_rate=round(win_rate, 2),
        avg_rrr=round(avg_rrr, 2),
        total_pnl=round(total_pnl, 2),
        profit_factor=round(profit_factor, 2),
        winning_trades=win_count,
        losing_trades=loss_count,
        total_profit=round(total_profit, 2),
        total_loss=round(total_loss, 2)
    )
