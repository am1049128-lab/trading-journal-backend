-- Create database
CREATE DATABASE trading_journal;

-- Connect to trading_journal database then run:

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Trades table
CREATE TABLE trades (
    trade_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    ticker VARCHAR(20) NOT NULL,
    trade_type VARCHAR(10) NOT NULL,
    strategy VARCHAR(100),
    entry_date TIMESTAMP WITH TIME ZONE NOT NULL,
    entry_price FLOAT NOT NULL,
    exit_date TIMESTAMP WITH TIME ZONE,
    exit_price FLOAT,
    lot_quantity INTEGER NOT NULL,
    stop_loss FLOAT,
    target_price FLOAT,
    notes TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trades_user_id ON trades(user_id);
CREATE INDEX idx_trades_ticker ON trades(ticker);
