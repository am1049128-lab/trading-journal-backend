# Trading Journal API

Stock Portfolio Tracker with Trading Journal and Analytics functionality.

## Features

- **User Authentication**: JWT-based auth with email/password
- **Trade Management**: Full CRUD operations for trades
- **Portfolio Analytics**: Win rate, PnL, profit factor, RRR calculations

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (python-jose)
- Bcrypt (passlib)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE trading_journal;
```

### 3. Environment Variables

Copy `.env.example` to `.env` and update:

```
DATABASE_URL=postgresql://username:password@localhost:5432/trading_journal
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload
```

API runs on `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns JWT token)
- `GET /auth/me` - Get current user info

### Trades

- `POST /trades/` - Create new trade
- `GET /trades/` - Get all user trades (pagination: skip, limit)
- `GET /trades/{trade_id}` - Get specific trade
- `PUT /trades/{trade_id}` - Update trade
- `DELETE /trades/{trade_id}` - Delete trade

### Analytics

- `GET /analytics/` - Get portfolio analytics

## Testing with Postman/curl

### Register User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "trader1",
    "email": "trader1@example.com",
    "password": "password123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=trader1&password=password123"
```

Response returns `access_token`. Use in subsequent requests:

### Create Trade

```bash
curl -X POST "http://localhost:8000/trades/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BBCA",
    "trade_type": "BUY",
    "strategy": "Breakout",
    "entry_date": "2024-01-15T10:30:00Z",
    "entry_price": 8500,
    "exit_date": "2024-01-16T15:45:00Z",
    "exit_price": 8750,
    "lot_quantity": 10,
    "stop_loss": 8300,
    "target_price": 8800,
    "notes": "Clean breakout above resistance"
  }'
```

### Get Analytics

```bash
curl -X GET "http://localhost:8000/analytics/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI interactive documentation.

## Database Schema

### Users Table

- user_id (PK)
- username (unique)
- email (unique)
- password_hash
- created_at

### Trades Table

- trade_id (PK)
- user_id (FK)
- ticker
- trade_type (BUY/SELL)
- strategy
- entry_date
- entry_price
- exit_date
- exit_price
- lot_quantity
- stop_loss
- target_price
- notes
- image_url
- created_at

## Analytics Calculations

- **Win Rate**: (winning_trades / total_closed_trades) * 100
- **Total PnL**: Sum of all profits - Sum of all losses
- **Profit Factor**: Total profit / Total loss
- **Avg RRR**: Average of (reward / risk) for trades with SL/TP set
