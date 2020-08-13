--
-- PostgreSQL database
--


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

--
-- Name: followdem; Type: SCHEMA; Schema: -; Owner: followdem
--

CREATE SCHEMA followdem;


------------
-- TABLES --
------------

--
-- Name: cor_animal_attributes; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.cor_animal_attributes (
    id_cor_an_att serial NOT NULL,
    id_attribute integer,
    id_animal integer,
    value character varying(120)
);

COMMENT ON TABLE followdem.cor_animal_attributes IS 'Table de correspondance entre un animal et ses attributs';


--
-- Name: cor_animal_devices; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.cor_animal_devices (
    id_cor_ad serial NOT NULL,
    id_animal integer,
    id_device integer,
    date_start timestamp without time zone,
    date_end timestamp without time zone,
    comment text
);

COMMENT ON TABLE followdem.cor_animal_devices IS 'Table de correspondance entre un animal et ses devices';


--
-- Name: t_animals; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.t_animals (
    id_animal serial NOT NULL,
    name character varying(50) NOT NULL,
    birth_year integer,
    capture_date timestamp without time zone,
    death_date timestamp without time zone,
    comment text,
    active BOOLEAN DEFAULT TRUE;
);

COMMENT ON TABLE followdem.t_animals IS 'Table contenant les animaux';


--
-- Name: lib_attributes; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.lib_attributes (
    id_attribute serial NOT NULL,
    attribute character varying(50) NOT NULL,
    value_list text,
    attribute_type character varying(50),
    "order" integer
);

COMMENT ON TABLE followdem.lib_attributes IS 'Table listant les attributs et leurs valeurs associées';

--
-- Name: lib_device_type; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.lib_device_type (
    id_device_type serial NOT NULL,
    device_type character varying(50) NOT NULL
);

COMMENT ON TABLE followdem.lib_device_type IS 'Table listant les types de device';

--
-- Name: t_devices; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.t_devices (
    id_device serial NOT NULL,
    ref_device character varying(50) NOT NULL,
    id_device_type integer NOT NULL,
    comment text
);

COMMENT ON TABLE followdem.t_devices IS 'Table listant les devices';

--
-- Name: t_gps_data; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.t_gps_data (
    id_gps_data serial NOT NULL,
    id_device integer NOT NULL,
    gps_date timestamp without time zone,
    ttf integer,
    temperature decimal,
    sat_number integer,
    hdop decimal,
    latitude decimal,
    longitude decimal,
    altitude decimal,
    dimension character varying(50),
    accurate boolean
);

COMMENT ON TABLE followdem.t_gps_data IS 'Table listant les données GPS d\un device';

--
-- Name: t_logs; Type: TABLE; Schema: followdem; Owner: followdem
--

CREATE TABLE followdem.t_logs (
    id_log serial NOT NULL,
    date timestamp without time zone,
    log timestamp without time zone
);

-----------------
-- PRIMARY KEY --
-----------------


ALTER TABLE ONLY followdem.cor_animal_attributes
    ADD CONSTRAINT cor_animal_attributes_pkey PRIMARY KEY (id_cor_an_att);

ALTER TABLE ONLY followdem.cor_animal_devices
    ADD CONSTRAINT cor_animal_devices_pkey PRIMARY KEY (id_cor_ad);

ALTER TABLE ONLY followdem.t_animals
    ADD CONSTRAINT t_animals_pkey PRIMARY KEY (id_animal);

ALTER TABLE ONLY followdem.lib_attributes
    ADD CONSTRAINT lib_attributes_pkey PRIMARY KEY (id_attribute);

ALTER TABLE ONLY followdem.lib_device_type
    ADD CONSTRAINT lib_device_type_pkey PRIMARY KEY (id_device_type);

ALTER TABLE ONLY followdem.t_devices
    ADD CONSTRAINT t_devices_pkey PRIMARY KEY (id_device);

ALTER TABLE ONLY followdem.t_gps_data
    ADD CONSTRAINT t_gps_data_pkey PRIMARY KEY (id_gps_data);

ALTER TABLE ONLY followdem.t_logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id_log);




------------------
-- UNIQUE INDEX --
------------------
CREATE UNIQUE INDEX device_type_idx ON followdem.lib_device_type (LOWER(device_type));
CREATE UNIQUE INDEX attribute_idx ON followdem.lib_attributes (LOWER(attribute));
CREATE UNIQUE INDEX name_unique_idx ON followdem.t_animals (LOWER(name));
CREATE UNIQUE INDEX ref_device_unique_idx ON followdem.t_devices (LOWER(ref_device));


-----------------
-- FOREIGN KEY --
-----------------

ALTER TABLE ONLY followdem.cor_animal_attributes
    ADD CONSTRAINT cor_animal_attributes_id_animal_fkey FOREIGN KEY (id_animal) REFERENCES followdem.t_animals(id_animal);
ALTER TABLE ONLY followdem.cor_animal_attributes
    ADD CONSTRAINT animal_attributes_id_attribute_fkey FOREIGN KEY (id_attribute) REFERENCES followdem.lib_attributes(id_attribute);


ALTER TABLE ONLY followdem.cor_animal_devices
    ADD CONSTRAINT cor_animal_devices_id_animal_fkey FOREIGN KEY (id_animal) REFERENCES followdem.t_animals(id_animal);
ALTER TABLE ONLY followdem.cor_animal_devices
    ADD CONSTRAINT cor_animal_devices_id_device_fkey FOREIGN KEY (id_device) REFERENCES followdem.t_devices(id_device);


ALTER TABLE ONLY followdem.t_devices
    ADD CONSTRAINT t_devices_id_device_type_fkey FOREIGN KEY (id_device_type) REFERENCES followdem.lib_device_type(id_device_type);


ALTER TABLE ONLY followdem.t_gps_data
    ADD CONSTRAINT t_gps_data_id_device_fkey FOREIGN KEY (id_device) REFERENCES followdem.t_devices(id_device);
