CREATE TABLE listings (
    id INTEGER PRIMARY KEY,
	listing_id VARCHAR(255) UNIQUE,
	price INT,
	title VARCHAR(255),
	url VARCHAR(255),
	bath_count INT,
	bedroom_count INT,
	reception_count INT,
	address VARCHAR(255),
	phone VARCHAR(255),
	created DATETIME DEFAULT CURRENT_TIMESTAMP
);
