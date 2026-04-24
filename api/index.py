from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logic
import json
import os

app = FastAPI(
    title="Global Energy Hub & Logistics Safety-Index API",
    description="Deterministic API for energy logistics, taxes, and route safety.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/route-safety-score")
async def get_route_safety(route_id: str):
    """
    Calculates safety score for a specific maritime route.
    """
    result = logic.calculate_route_safety(route_id)
    if not result:
        raise HTTPException(status_code=404, detail="Route not found")
    return result

@app.get("/api/energy-tax-logic")
async def get_energy_tax(
    country: str, 
    quantity: float = Query(..., description="Quantity in cubic meters (m3)"),
    months: int = Query(0, description="Months of storage"),
    value: float = Query(800.0, description="Base value per m3 in USD")
):
    """
    Calculates taxes and storage fees for energy products by country.
    """
    result = logic.calculate_energy_tax(country, quantity, months, value)
    if not result:
        raise HTTPException(status_code=404, detail="Country tax data not found")
    return result

@app.get("/api/port-infrastructure-specs")
async def get_port_specs(port: str):
    """
    Provides technical specifications for major energy ports.
    """
    result = logic.get_port_specs(port)
    if not result:
        raise HTTPException(status_code=404, detail="Port not found")
    return result

@app.get("/api/market-prices")
async def get_market_prices():
    """
    Returns latest energy prices ( Brent, WTI, etc.) synced from EIA/IEA.
    """
    try:
        prices = logic.load_json('prices.json')
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "operational", "engine": "Deterministic Logic Layer v1"}

# Static files are now served from the /public directory by Vercel directly
