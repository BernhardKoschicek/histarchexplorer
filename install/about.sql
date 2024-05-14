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
	description TEXT);


ALTER TABLE tng.config ADD CONSTRAINT config_config_classes_fk FOREIGN KEY (config_class) REFERENCES tng.config_classes(id);
ALTER TABLE tng.links ADD CONSTRAINT links_config_properties_fk FOREIGN KEY (property) REFERENCES tng.config_properties(id);
ALTER TABLE tng.links ADD CONSTRAINT links_config_fk_domain FOREIGN KEY (domain_id) REFERENCES tng.config(id);
ALTER TABLE tng.links ADD CONSTRAINT links_config_fk_range FOREIGN KEY (range_id) REFERENCES tng.config(id);
ALTER TABLE tng.links ADD CONSTRAINT links_config_fk_role FOREIGN KEY (role) REFERENCES tng.config(id);

CREATE OR REPLACE FUNCTION tng.delete_links_on_config_delete()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    DELETE FROM tng.links WHERE domain_id = OLD.id OR range_id = OLD.id;
    RETURN OLD;
END;
$function$;

create trigger delete_links_trigger before
delete
    on
    tng.config for each row execute function tng.delete_links_on_config_delete();




