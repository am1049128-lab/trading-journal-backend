from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from database.db import Base

class Trade(Base):
    __tablename__ = "trades"
    
    trade_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    ticker = Column(String(20), nullable=False)
    trade_type = Column(String(10), nullable=False)  # 'BUY' or 'SELL'
    strategy = Column(String(100))
    entry_date = Column(DateTime(timezone=True), nullable=False)
    entry_price = Column(Float, nullable=False)
    exit_date = Column(DateTime(timezone=True))
    exit_price = Column(Float)
    lot_quantity = Column(Integer, nullable=False)
    stop_loss = Column(Float)
    target_price = Column(Float)
    notes = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
