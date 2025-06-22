--
-- PostgreSQL database dump
--

-- Dumped from database version 15.10 (Debian 15.10-0+deb12u1)
-- Dumped by pg_dump version 15.10 (Debian 15.10-0+deb12u1)

-- Started on 2025-06-22 15:27:59 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY tng.links DROP CONSTRAINT IF EXISTS links_config_properties_fk;
ALTER TABLE IF EXISTS ONLY tng.links DROP CONSTRAINT IF EXISTS links_config_fk_role;
ALTER TABLE IF EXISTS ONLY tng.links DROP CONSTRAINT IF EXISTS links_config_fk_range;
ALTER TABLE IF EXISTS ONLY tng.links DROP CONSTRAINT IF EXISTS links_config_fk_domain;
ALTER TABLE IF EXISTS ONLY tng.config DROP CONSTRAINT IF EXISTS config_config_classes_fk;
DROP TRIGGER IF EXISTS delete_links_trigger ON tng.config;
ALTER TABLE IF EXISTS ONLY tng.settings DROP CONSTRAINT IF EXISTS settings_pkey;
ALTER TABLE IF EXISTS ONLY tng.maps DROP CONSTRAINT IF EXISTS maps_pkey;
ALTER TABLE IF EXISTS ONLY tng.links DROP CONSTRAINT IF EXISTS links_pkey;
ALTER TABLE IF EXISTS ONLY tng.config_properties DROP CONSTRAINT IF EXISTS config_properties_pkey;
ALTER TABLE IF EXISTS ONLY tng.config DROP CONSTRAINT IF EXISTS config_pkey;
ALTER TABLE IF EXISTS ONLY tng.config_classes DROP CONSTRAINT IF EXISTS config_classes_pkey;
ALTER TABLE IF EXISTS tng.settings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS tng.maps ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS tng.links ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS tng.config_properties ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS tng.config_classes ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS tng.config ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS tng.settings_id_seq;
DROP TABLE IF EXISTS tng.settings;
DROP SEQUENCE IF EXISTS tng.maps_id_seq;
DROP TABLE IF EXISTS tng.maps;
DROP SEQUENCE IF EXISTS tng.links_id_seq;
DROP TABLE IF EXISTS tng.links;
DROP SEQUENCE IF EXISTS tng.config_properties_id_seq;
DROP TABLE IF EXISTS tng.config_properties;
DROP SEQUENCE IF EXISTS tng.config_id_seq;
DROP SEQUENCE IF EXISTS tng.config_classes_id_seq;
DROP TABLE IF EXISTS tng.config_classes;
DROP TABLE IF EXISTS tng.config;
DROP FUNCTION IF EXISTS tng.getdates(first timestamp without time zone, last timestamp without time zone, comment text);
DROP FUNCTION IF EXISTS tng.delete_links_on_config_delete();
DROP SCHEMA IF EXISTS tng;
--
-- TOC entry 16 (class 2615 OID 1329126)
-- Name: tng; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA tng;


--
-- TOC entry 1183 (class 1255 OID 1329127)
-- Name: delete_links_on_config_delete(); Type: FUNCTION; Schema: tng; Owner: -
--

CREATE FUNCTION tng.delete_links_on_config_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            DELETE FROM tng.links WHERE domain_id = OLD.id OR range_id =
            OLD.id;
            RETURN OLD;
        END;
        $$;


--
-- TOC entry 1184 (class 1255 OID 1329128)
-- Name: getdates(timestamp without time zone, timestamp without time zone, text); Type: FUNCTION; Schema: tng; Owner: -
--

CREATE FUNCTION tng.getdates(first timestamp without time zone, last timestamp without time zone, comment text) RETURNS text
    LANGUAGE plpgsql
    AS $$
        DECLARE
            return_date TEXT;
        BEGIN
            CASE
                WHEN comment LIKE '-%' THEN
                    -- Use the comment as a negative year with leading zeros
                    SELECT TO_CHAR(comment::INTEGER, 'FM000000000') INTO return_date;
                ELSE
                    -- Use the date logic
                    SELECT TO_CHAR(LEAST(first, last), 'FM00000YYYY-MM-DD') INTO return_date;
                CASE WHEN EXTRACT(YEAR FROM (LEAST(first, last)::DATE)) < 1 THEN SELECT '-' || return_date INTO return_date; ELSE NULL; END CASE;
            END CASE;

            RETURN return_date;
        END;
        $$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 384 (class 1259 OID 1329129)
-- Name: config; Type: TABLE; Schema: tng; Owner: -
--

CREATE TABLE tng.config (
    id integer NOT NULL,
    name jsonb,
    description jsonb,
    address jsonb,
    config_class integer,
    email text,
    orcid_id text,
    image text,
    website text,
    legal_notice jsonb,
    imprint jsonb
);


--
-- TOC entry 385 (class 1259 OID 1329134)
-- Name: config_classes; Type: TABLE; Schema: tng; Owner: -
--

CREATE TABLE tng.config_classes (
    id integer NOT NULL,
    name text,
    description text
);


--
-- TOC entry 386 (class 1259 OID 1329139)
-- Name: config_classes_id_seq; Type: SEQUENCE; Schema: tng; Owner: -
--

CREATE SEQUENCE tng.config_classes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4760 (class 0 OID 0)
-- Dependencies: 386
-- Name: config_classes_id_seq; Type: SEQUENCE OWNED BY; Schema: tng; Owner: -
--

ALTER SEQUENCE tng.config_classes_id_seq OWNED BY tng.config_classes.id;


--
-- TOC entry 387 (class 1259 OID 1329140)
-- Name: config_id_seq; Type: SEQUENCE; Schema: tng; Owner: -
--

CREATE SEQUENCE tng.config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4761 (class 0 OID 0)
-- Dependencies: 387
-- Name: config_id_seq; Type: SEQUENCE OWNED BY; Schema: tng; Owner: -
--

ALTER SEQUENCE tng.config_id_seq OWNED BY tng.config.id;


--
-- TOC entry 388 (class 1259 OID 1329141)
-- Name: config_properties; Type: TABLE; Schema: tng; Owner: -
--

CREATE TABLE tng.config_properties (
    id integer NOT NULL,
    name jsonb,
    name_inv jsonb,
    description jsonb,
    domain integer,
    range integer
);


--
-- TOC entry 389 (class 1259 OID 1329146)
-- Name: config_properties_id_seq; Type: SEQUENCE; Schema: tng; Owner: -
--

CREATE SEQUENCE tng.config_properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4762 (class 0 OID 0)
-- Dependencies: 389
-- Name: config_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: tng; Owner: -
--

ALTER SEQUENCE tng.config_properties_id_seq OWNED BY tng.config_properties.id;


--
-- TOC entry 390 (class 1259 OID 1329147)
-- Name: links; Type: TABLE; Schema: tng; Owner: -
--

CREATE TABLE tng.links (
    id integer NOT NULL,
    domain_id integer,
    range_id integer,
    property integer,
    attribute integer,
    sortorder integer
);


--
-- TOC entry 391 (class 1259 OID 1329150)
-- Name: links_id_seq; Type: SEQUENCE; Schema: tng; Owner: -
--

CREATE SEQUENCE tng.links_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4763 (class 0 OID 0)
-- Dependencies: 391
-- Name: links_id_seq; Type: SEQUENCE OWNED BY; Schema: tng; Owner: -
--

ALTER SEQUENCE tng.links_id_seq OWNED BY tng.links.id;


--
-- TOC entry 392 (class 1259 OID 1329151)
-- Name: maps; Type: TABLE; Schema: tng; Owner: -
--

CREATE TABLE tng.maps (
    id integer NOT NULL,
    name text,
    display_name text,
    tilestring text,
    sortorder integer
);


--
-- TOC entry 393 (class 1259 OID 1329156)
-- Name: maps_id_seq; Type: SEQUENCE; Schema: tng; Owner: -
--

CREATE SEQUENCE tng.maps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4764 (class 0 OID 0)
-- Dependencies: 393
-- Name: maps_id_seq; Type: SEQUENCE OWNED BY; Schema: tng; Owner: -
--

ALTER SEQUENCE tng.maps_id_seq OWNED BY tng.maps.id;


--
-- TOC entry 394 (class 1259 OID 1329157)
-- Name: settings; Type: TABLE; Schema: tng; Owner: -
--

CREATE TABLE tng.settings (
    id integer NOT NULL,
    index_img text,
    index_map integer,
    img_map text,
    greyscale boolean,
    shown_entities text[],
    shown_types text[],
    hidden_entities text[],
    hidden_types text[],
    shown_ids text[],
    hidden_ids text[]
);


--
-- TOC entry 395 (class 1259 OID 1329162)
-- Name: settings_id_seq; Type: SEQUENCE; Schema: tng; Owner: -
--

CREATE SEQUENCE tng.settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4765 (class 0 OID 0)
-- Dependencies: 395
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: tng; Owner: -
--

ALTER SEQUENCE tng.settings_id_seq OWNED BY tng.settings.id;


--
-- TOC entry 4571 (class 2604 OID 1329163)
-- Name: config id; Type: DEFAULT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config ALTER COLUMN id SET DEFAULT nextval('tng.config_id_seq'::regclass);


--
-- TOC entry 4572 (class 2604 OID 1329164)
-- Name: config_classes id; Type: DEFAULT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config_classes ALTER COLUMN id SET DEFAULT nextval('tng.config_classes_id_seq'::regclass);


--
-- TOC entry 4573 (class 2604 OID 1329165)
-- Name: config_properties id; Type: DEFAULT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config_properties ALTER COLUMN id SET DEFAULT nextval('tng.config_properties_id_seq'::regclass);


--
-- TOC entry 4574 (class 2604 OID 1329166)
-- Name: links id; Type: DEFAULT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.links ALTER COLUMN id SET DEFAULT nextval('tng.links_id_seq'::regclass);


--
-- TOC entry 4575 (class 2604 OID 1329167)
-- Name: maps id; Type: DEFAULT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.maps ALTER COLUMN id SET DEFAULT nextval('tng.maps_id_seq'::regclass);


--
-- TOC entry 4576 (class 2604 OID 1329168)
-- Name: settings id; Type: DEFAULT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.settings ALTER COLUMN id SET DEFAULT nextval('tng.settings_id_seq'::regclass);


--
-- TOC entry 4743 (class 0 OID 1329129)
-- Dependencies: 384
-- Data for Name: config; Type: TABLE DATA; Schema: tng; Owner: -
--

INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (2, '{"de": "Stefan Eichert", "en": "Stefan Eichert"}', NULL, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (3, '{"de": "Lisa Aldrian", "en": "Lisa Aldrian"}', NULL, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (4, '{"de": "David Ruß", "en": "David Ruß"}', NULL, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (5, '{"de": "Projektleitung", "en": "Principal Investigator"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (6, '{"de": "Hauptkoordinator", "en": "Main Coordinator"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (7, '{"de": "Forscher", "en": "Researcher"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (8, '{"de": "Softwareentwickler", "en": "Software Developer"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (9, '{"de": "Design & Programmierung", "en": "Design & Programming"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (10, '{"de": "Archäologe", "en": "Archaeologist"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (11, '{"de": "Anthropologe", "en": "Anthropologist"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (12, '{"de": "Datenaufnahme", "en": "Data Acquisition"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (13, '{"de": "Historiker", "en": "Historian"}', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (14, '{"de": "Sponsor", "en": "Sponsor"}', NULL, NULL, 3, 'https://example.example', NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (15, '{"de": "Partner", "en": "Partner"}', NULL, NULL, 3, 'https://example.example', NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (17, '{"de": "RELIC", "en": "RELIC"}', NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (18, '{"de": "REPLICO", "en": "REPLICO"}', NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (20, '{"de": "Universität Wien", "en": "University of Vienna"}', '{"de": "Die Wiener Uni", "en": "Viennese university"}', '{"de": "Universitätsring 1\r\n1010 Wien", "en": "Universitätsring 1\r\n1010 Vienna"}', 4, 'uni@univie.ac.at', NULL, 'https://www.univie.ac.at/fileadmin/templates/Startseite/assets/uni_logo_220@2x.jpg', 'https://www.univie.ac.at/', '{}', '{}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (1, '{"de": "HistArchExplorer ", "en": "HistArchExplorer "}', '{"de": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  \r\n\r\nDuis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.  \r\n\r\nUt wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.  \r\n\r\nNam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.  \r\n\r\nDuis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis.   \r\n\r\nAt vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam"}', '{}', 5, NULL, NULL, NULL, 'http://127.0.0.1:5000/', '{"de": "Ich auch nicht"}', '{"de": "Hab ich keins"}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (21, '{"de": "Austrian Centre for Digital Humanities", "en": "Austrian Centre for Digital Humanities & Cultural Heritage"}', '{"de": "Digitale Geisteswissenschaften"}', '{"de": "Bäckerstraße 13\r\n1010 Wien"}', 4, 'ACDH-CH-Office@oeaw.ac.at', NULL, 'https://www.oeaw.ac.at/fileadmin/oeaw/institutstemplate/acdh/img/acdh-ch-logo96.png', 'https://www.oeaw.ac.at/acdh/acdh-ch-home', '{}', '{}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (22, '{"de": "Nina Brundke", "en": "Nina Richards"}', '{"de": "Beste Anthropologin", "en": "Best anthropologist! "}', '{"en": "Burgring 7"}', 2, 'nina@richards.us', NULL, NULL, NULL, '{}', '{}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (23, '{"de": "Physiotherapeut"}', '{}', '{}', 3, NULL, NULL, NULL, NULL, '{}', '{}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (19, '{"de": "NHM", "en": "NHM_"}', '{"de": "Naturhistorisches Museum"}', '{"de": "Burgring 7"}', 4, NULL, NULL, 'https://nhm.at/jart/prj3/nhm-resp/resources/images/logo.svg', 'https://nhm.at/', '{}', '{}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (24, '{"de": "FH Wien"}', '{}', '{}', 4, NULL, NULL, NULL, NULL, '{}', '{}') ON CONFLICT DO NOTHING;
INSERT INTO tng.config (id, name, description, address, config_class, email, orcid_id, image, website, legal_notice, imprint) VALUES (16, '{"de": "THANADOS", "en": "THANADOS"}', '{}', '{}', 1, NULL, NULL, NULL, 'https://thanados.net/', '{}', '{}') ON CONFLICT DO NOTHING;


--
-- TOC entry 4744 (class 0 OID 1329134)
-- Dependencies: 385
-- Data for Name: config_classes; Type: TABLE DATA; Schema: tng; Owner: -
--

INSERT INTO tng.config_classes (id, name, description) VALUES (1, 'project', NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_classes (id, name, description) VALUES (2, 'person', NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_classes (id, name, description) VALUES (3, 'role', NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_classes (id, name, description) VALUES (4, 'institution', NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_classes (id, name, description) VALUES (5, 'main-project', NULL) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_classes (id, name, description) VALUES (6, 'language_code', NULL) ON CONFLICT DO NOTHING;


--
-- TOC entry 4747 (class 0 OID 1329141)
-- Dependencies: 388
-- Data for Name: config_properties; Type: TABLE DATA; Schema: tng; Owner: -
--

INSERT INTO tng.config_properties (id, name, name_inv, description, domain, range) VALUES (1, '{"de": "hat Mitglied", "en": "has member"}', '{"de": "ist Mitglied von", "en": "is member of"}', NULL, 1, 2) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_properties (id, name, name_inv, description, domain, range) VALUES (2, '{"de": "hat Zugehörigkeit", "en": "has affiliation"}', '{"de": "ist Zugehörigkeit von", "en": "is affiliation of"}', NULL, 2, 4) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_properties (id, name, name_inv, description, domain, range) VALUES (3, '{"de": "hat Kernmitglied", "en": "has core member"}', '{"de": "ist Kernmitglied von", "en": "is core member of"}', NULL, 5, 2) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_properties (id, name, name_inv, description, domain, range) VALUES (4, '{"de": "hat Kerninstitution", "en": "has core institution"}', '{"de": "ist Kerninstitution von", "en": "is core institution of"}', NULL, 5, 4) ON CONFLICT DO NOTHING;
INSERT INTO tng.config_properties (id, name, name_inv, description, domain, range) VALUES (5, '{"de": "hat Institution", "en": "has institution"}', '{"de": "ist Institution von", "en": "is institution of"}', NULL, 1, 4) ON CONFLICT DO NOTHING;


--
-- TOC entry 4749 (class 0 OID 1329147)
-- Dependencies: 390
-- Data for Name: links; Type: TABLE DATA; Schema: tng; Owner: -
--

INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (1, 1, 22, 3, 5, 1) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (2, 22, 19, 2, 11, 2) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (3, 22, 21, 2, 5, 3) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (4, 16, 22, 1, 12, 4) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (5, 18, 22, 1, 5, 5) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (6, 17, 22, 1, 10, 6) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (7, 3, 19, 2, 8, 7) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (8, 3, 24, 2, 23, 8) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (9, 17, 3, 1, 12, 9) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (10, 1, 3, 3, 8, 10) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (11, 4, 19, 2, 10, 11) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (12, 18, 4, 1, 13, 12) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (13, 17, 4, 1, 10, 13) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (14, 1, 4, 3, 12, 14) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (15, 2, 19, 2, 5, 15) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (16, 2, 19, 2, 10, 16) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (17, 2, 19, 2, 8, 17) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (18, 16, 2, 1, 5, 18) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (19, 16, 2, 1, 8, 19) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (20, 1, 2, 3, 5, 20) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (21, 4, 20, 2, 13, 21) ON CONFLICT DO NOTHING;
INSERT INTO tng.links (id, domain_id, range_id, property, attribute, sortorder) VALUES (22, 16, 20, 5, 14, 22) ON CONFLICT DO NOTHING;


--
-- TOC entry 4751 (class 0 OID 1329151)
-- Dependencies: 392
-- Data for Name: maps; Type: TABLE DATA; Schema: tng; Owner: -
--

INSERT INTO tng.maps (id, name, display_name, tilestring, sortorder) VALUES (1, 'OpenStreetMap', 'Open Street Map', 'L.tileLayer(
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png", {maxZoom: 19, attribution: ''&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors''});', 1) ON CONFLICT DO NOTHING;


--
-- TOC entry 4753 (class 0 OID 1329157)
-- Dependencies: 394
-- Data for Name: settings; Type: TABLE DATA; Schema: tng; Owner: -
--

INSERT INTO tng.settings (id, index_img, index_map, img_map, greyscale, shown_entities, shown_types, hidden_entities, hidden_types, shown_ids, hidden_ids) VALUES (1, '/static/images/index_map_bg/Blank_map_of_Europe_central_network.png', 1, 'map', false, '{person,group,artifact,human_remains,acquisition,event,activity,creation,move,production,modification,place,stratigraphic_unit,feature,source,bibliography,external_reference,edition,file}', NULL, '{group,stratigraphic_unit,source,external_reference}', NULL, NULL, NULL) ON CONFLICT DO NOTHING;


--
-- TOC entry 4766 (class 0 OID 0)
-- Dependencies: 386
-- Name: config_classes_id_seq; Type: SEQUENCE SET; Schema: tng; Owner: -
--

SELECT pg_catalog.setval('tng.config_classes_id_seq', 6, true);


--
-- TOC entry 4767 (class 0 OID 0)
-- Dependencies: 387
-- Name: config_id_seq; Type: SEQUENCE SET; Schema: tng; Owner: -
--

SELECT pg_catalog.setval('tng.config_id_seq', 24, true);


--
-- TOC entry 4768 (class 0 OID 0)
-- Dependencies: 389
-- Name: config_properties_id_seq; Type: SEQUENCE SET; Schema: tng; Owner: -
--

SELECT pg_catalog.setval('tng.config_properties_id_seq', 5, true);


--
-- TOC entry 4769 (class 0 OID 0)
-- Dependencies: 391
-- Name: links_id_seq; Type: SEQUENCE SET; Schema: tng; Owner: -
--

SELECT pg_catalog.setval('tng.links_id_seq', 22, true);


--
-- TOC entry 4770 (class 0 OID 0)
-- Dependencies: 393
-- Name: maps_id_seq; Type: SEQUENCE SET; Schema: tng; Owner: -
--

SELECT pg_catalog.setval('tng.maps_id_seq', 1, true);


--
-- TOC entry 4771 (class 0 OID 0)
-- Dependencies: 395
-- Name: settings_id_seq; Type: SEQUENCE SET; Schema: tng; Owner: -
--

SELECT pg_catalog.setval('tng.settings_id_seq', 1, true);


--
-- TOC entry 4580 (class 2606 OID 1329170)
-- Name: config_classes config_classes_pkey; Type: CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config_classes
    ADD CONSTRAINT config_classes_pkey PRIMARY KEY (id);


--
-- TOC entry 4578 (class 2606 OID 1329172)
-- Name: config config_pkey; Type: CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config
    ADD CONSTRAINT config_pkey PRIMARY KEY (id);


--
-- TOC entry 4582 (class 2606 OID 1329174)
-- Name: config_properties config_properties_pkey; Type: CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config_properties
    ADD CONSTRAINT config_properties_pkey PRIMARY KEY (id);


--
-- TOC entry 4584 (class 2606 OID 1329176)
-- Name: links links_pkey; Type: CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.links
    ADD CONSTRAINT links_pkey PRIMARY KEY (id);


--
-- TOC entry 4586 (class 2606 OID 1329178)
-- Name: maps maps_pkey; Type: CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.maps
    ADD CONSTRAINT maps_pkey PRIMARY KEY (id);


--
-- TOC entry 4588 (class 2606 OID 1329180)
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- TOC entry 4594 (class 2620 OID 1329181)
-- Name: config delete_links_trigger; Type: TRIGGER; Schema: tng; Owner: -
--

CREATE TRIGGER delete_links_trigger BEFORE DELETE ON tng.config FOR EACH ROW EXECUTE FUNCTION tng.delete_links_on_config_delete();


--
-- TOC entry 4589 (class 2606 OID 1329182)
-- Name: config config_config_classes_fk; Type: FK CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.config
    ADD CONSTRAINT config_config_classes_fk FOREIGN KEY (config_class) REFERENCES tng.config_classes(id);


--
-- TOC entry 4590 (class 2606 OID 1329187)
-- Name: links links_config_fk_domain; Type: FK CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.links
    ADD CONSTRAINT links_config_fk_domain FOREIGN KEY (domain_id) REFERENCES tng.config(id);


--
-- TOC entry 4591 (class 2606 OID 1329192)
-- Name: links links_config_fk_range; Type: FK CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.links
    ADD CONSTRAINT links_config_fk_range FOREIGN KEY (range_id) REFERENCES tng.config(id);


--
-- TOC entry 4592 (class 2606 OID 1329197)
-- Name: links links_config_fk_role; Type: FK CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.links
    ADD CONSTRAINT links_config_fk_role FOREIGN KEY (attribute) REFERENCES tng.config(id);


--
-- TOC entry 4593 (class 2606 OID 1329202)
-- Name: links links_config_properties_fk; Type: FK CONSTRAINT; Schema: tng; Owner: -
--

ALTER TABLE ONLY tng.links
    ADD CONSTRAINT links_config_properties_fk FOREIGN KEY (property) REFERENCES tng.config_properties(id);


-- Completed on 2025-06-22 15:27:59 CEST

--
-- PostgreSQL database dump complete
--

