DROP SCHEMA IF EXISTS tng CASCADE;
CREATE SCHEMA IF NOT EXISTS tng;

CREATE TABLE IF NOT EXISTS tng.config (
    id SERIAL PRIMARY KEY,
  	name TEXT,
    description TEXT,
   	address TEXT,
    config_class INT,
    email TEXT,
    orcid_id TEXT,
    image TEXT,
    website TEXT,
    language TEXT DEFAULT 'en'
);

CREATE TABLE IF NOT EXISTS tng.links (
 	id SERIAL PRIMARY KEY,
	domain_id INT,
	range_id INT,
	property INT
	);

CREATE TABLE IF NOT EXISTS tng.config_classes (
	id SERIAL PRIMARY KEY,
	name TEXT,
	description TEXT);

CREATE TABLE IF NOT EXISTS tng.config_properties (
	id SERIAL PRIMARY KEY,
	name TEXT,
	description TEXT
	)




