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


def get_all_listings(conn=conn) -> list:
	cursor = conn.cursor()
	rows = cursor.execute("SELECT * FROM listings").fetchall()

	return to_listings(rows)


def get_listing_by_id(id : int, conn=conn) -> Listing:
	cursor = conn.cursor()
	rows = cursor.execute(f"SELECT * FROM listings WHERE id = \"{id}\"").fetchone()

	return to_listing(rows)


def to_listings(rows) -> list:
	results = []
	for r in rows: 
		results.append(to_listing(r))
	
	return results


def to_listing(row) -> Listing:
	f = Listing(*row[1:])

	f.id = row[0]

	return f