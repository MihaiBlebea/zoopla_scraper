import sqlite3

from models import Listing

conn = sqlite3.connect("store.db")

def insert_listing(listing : Listing, conn=conn) -> Listing:
	cursor = conn.cursor()
	query = """INSERT OR IGNORE INTO listings 
	(listing_id, price, title, url, bath_count, bedroom_count, reception_count, address, phone) 
	VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")""".format(
		listing.listing_id,
		listing.price,
		listing.title,
		listing.url,
		listing.bath_count,
		listing.bedroom_count,
		listing.reception_count,
		listing.address,
		listing.phone,
	)
	
	cursor.execute(query)

	conn.commit()

	listing.id = cursor.lastrowid

	cursor.close()

	return listing