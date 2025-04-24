from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from app.modules.user.user_model import UserModel
from app.modules.stock.stock_model import StockModel

import yfinance as yf
import requests
from bs4 import BeautifulSoup

router = APIRouter()



@router.get("/api/portfolio-stocks")
async def get_portfolio_stocks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    results = []
    
    # Query the database for the user's stock symbols
    user_stocks = db.query(StockModel.symbol).filter(StockModel.user_id == current_user.user_id, StockModel.is_active == True, StockModel.is_deleted == False).distinct().all()
    user_symbols = [stock.symbol for stock in user_stocks]

    if not user_symbols:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No stocks found for the user.")

    # Fetch stock data for the user's symbols
    tickers = yf.Tickers(" ".join(user_symbols))

    for symbol in user_symbols:
        try:
            info = tickers.tickers[symbol].info
            if not info or info.get("quoteType") is None:
                continue

            # Get the quantity from the database
            stock = db.query(StockModel).filter(StockModel.symbol == symbol, StockModel.user_id == current_user.user_id).first()
            
            results.append({
                "symbol": symbol,
                "name": info.get("shortName", symbol),
                "purchasePrice": info.get("currentPrice", 0.0),
                "quantity": stock.quantity if stock else 0,  # Get actual quantity
                "exchange": info.get("exchange", "Unknown")
            })
        except Exception as e:
            results.append({
                "symbol": symbol,
                "name": "Error",
                "purchasePrice": 0,
                "quantity": 0,
                "exchange": "Error"
            })

    return results



@router.get("/api/stock-data")
async def get_stock_data(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Validate stock symbol
        if not info or info.get("quoteType") is None:
            raise ValueError("Invalid stock symbol")

        cmp = info.get("currentPrice", 0.0)
        pe_ratio = info.get("trailingPE", "N/A")
        earnings = info.get("epsTrailingTwelveMonths", "N/A")
        sector = info.get("sector", "Unknown Sector")
        

        return {
            "cmp": float(cmp),
            "peRatio": pe_ratio,
            "earnings": earnings,
            "sector": sector
        }
    except Exception as e:
        return {"error": str(e)}
