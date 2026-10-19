#!/usr/bin/env python
"""
Quick setup and test script for Trading Journal API
"""
import sys
import os

print("=== Trading Journal API Setup Test ===\n")

# Test imports
print("1. Testing imports...")
try:
    from models import User, Trade, TradeCreate, AnalyticsResponse
    from auth import jwt_handler
    from database import Base, engine
    print("   ✓ All imports successful\n")
except ImportError as e:
    print(f"   ✗ Import failed: {e}\n")
    sys.exit(1)

# Check environment
print("2. Checking environment...")
if not os.path.exists(".env"):
    print("   ⚠ .env file not found. Copy .env.example to .env and configure:\n")
    print("     DATABASE_URL=postgresql://user:pass@localhost:5432/trading_journal")
    print("     SECRET_KEY=your-secret-key-here\n")
else:
    print("   ✓ .env file exists\n")

# Check database connection
print("3. Testing database connection...")
try:
    from sqlalchemy import text
    from database import SessionLocal
    
    db = SessionLocal()
    result = db.execute(text("SELECT 1"))
    db.close()
    print("   ✓ Database connection successful\n")
except Exception as e:
    print(f"   ✗ Database connection failed: {e}")
    print("   Make sure PostgreSQL is running and DATABASE_URL is correct\n")

print("=== Setup Complete ===")
print("\nTo start the server:")
print("  python main.py")
print("\nAPI Documentation:")
print("  http://localhost:8000/docs")
