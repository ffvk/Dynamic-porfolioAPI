from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from app.modules.user.user_model import UserModel
import yfinance as yf
import requests
from bs4 import BeautifulSoup

router = APIRouter()





router = APIRouter()

# @router.get("/api/stock-data")
# async def get_stock_data(symbol: str):
#     try:
#         ticker = yf.Ticker(symbol)
#         cmp = ticker.info.get("currentPrice", 0.0)

#         # Simulate scraping Google Finance for P/E ratio and earnings (example only)
#         url = f"https://www.google.com/finance/quote/{symbol}:NSE"
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")

#         pe_ratio = soup.find("div", string="P/E ratio").find_next("div").text
#         earnings = soup.find("div", string="Earnings per share").find_next("div").text

#         return {
#             "cmp": float(cmp),
#             "peRatio": pe_ratio,
#             "earnings": earnings
#         }
#     except Exception as e:
#         return {"error": str(e)}



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
