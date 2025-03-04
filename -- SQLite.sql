-- SQLite
PRAGMA table_info(merchexchangeapi_listing);

PRAGMA foreign_keys=off;
ALTER TABLE merchexchangeapi_listing RENAME TO temp_listing;
CREATE TABLE merchexchangeapi_listing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50),
    artist_id INTEGER,
    category_id INTEGER,
    description VARCHAR(280),
    price DECIMAL(6,2),
    size VARCHAR(50),
    condition VARCHAR(50),
    image VARCHAR(200),
    created_by_id INTEGER,
    created_at DATETIME,
    published BOOLEAN,
    sold BOOLEAN,
    FOREIGN KEY(artist_id) REFERENCES merchexchangeapi_artist(id),
    FOREIGN KEY(category_id) REFERENCES merchexchangeapi_category(id),
    FOREIGN KEY(created_by_id) REFERENCES merchexchangeapi_user(id)
);
INSERT INTO merchexchangeapi_listing SELECT id, title, artist_id, category_id, description, price, size, condition, image, created_by_id, created_at, published, sold FROM temp_listing;
DROP TABLE temp_listing;
PRAGMA foreign_keys=on;
