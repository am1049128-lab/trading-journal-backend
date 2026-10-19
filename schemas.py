from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# User schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Trade schemas
class TradeCreate(BaseModel):
    ticker: str = Field(..., max_length=20)
    trade_type: str = Field(..., pattern="^(BUY|SELL)$")
    strategy: Optional[str] = Field(None, max_length=100)
    entry_date: datetime
    entry_price: float = Field(..., gt=0)
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = Field(None, gt=0)
    lot_quantity: int = Field(..., gt=0)
    stop_loss: Optional[float] = Field(None, gt=0)
    target_price: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)

class TradeUpdate(BaseModel):
    ticker: Optional[str] = Field(None, max_length=20)
    trade_type: Optional[str] = Field(None, pattern="^(BUY|SELL)$")
    strategy: Optional[str] = Field(None, max_length=100)
    entry_date: Optional[datetime] = None
    entry_price: Optional[float] = Field(None, gt=0)
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = Field(None, gt=0)
    lot_quantity: Optional[int] = Field(None, gt=0)
    stop_loss: Optional[float] = Field(None, gt=0)
    target_price: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)

class TradeResponse(BaseModel):
    trade_id: int
    user_id: int
    ticker: str
    trade_type: str
    strategy: Optional[str]
    entry_date: datetime
    entry_price: float
    exit_date: Optional[datetime]
    exit_price: Optional[float]
    lot_quantity: int
    stop_loss: Optional[float]
    target_price: Optional[float]
    notes: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analytics schemas
class AnalyticsResponse(BaseModel):
    total_trades: int
    closed_trades: int
    win_rate: float
    avg_rrr: float
    total_pnl: float
    profit_factor: float
    winning_trades: int
    losing_trades: int
    total_profit: float
    total_loss: float
