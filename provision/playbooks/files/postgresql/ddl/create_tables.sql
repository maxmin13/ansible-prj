
CREATE TABLE IF NOT EXISTS migrations (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(50) UNIQUE NOT NULL,  
	run_on TIMESTAMP default current_timestamp NOT NULL);

CREATE TABLE IF NOT EXISTS accounts (
	id SERIAL PRIMARY KEY, 
	username VARCHAR(50) UNIQUE NOT NULL, 
	password VARCHAR(50) NOT NULL, 
	email VARCHAR(255) UNIQUE NOT NULL, 
	created_on TIMESTAMP default current_timestamp NOT NULL,
	last_login TIMESTAMP);

INSERT INTO migrations(name) VALUES('create_tables');