from fastapi import FastAPI
import sys

sys.path.append("./src")

from store import get_all_listings, get_listing_by_id


app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.get("/listings")
async def listings(price_from: int = 0, price_to: int = None):
	return get_all_listings()


@app.get("/listing/{id}")
async def listings(id):
	return get_listing_by_id(id)