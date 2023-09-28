-- Database: cars

-- DROP DATABASE IF EXISTS cars;

CREATE DATABASE Detection
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Arabic_Saudi Arabia.1256'
    LC_CTYPE = 'Arabic_Saudi Arabia.1256'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- CREATE TABLE car_table
CREATE TABLE cars(
    id serial PRIMARY KEY,
    plate_number VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);