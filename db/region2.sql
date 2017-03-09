--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

-- Started on 2017-02-03 12:28:43

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12387)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2125 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 185 (class 1259 OID 16809)
-- Name: region2_votes; Type: TABLE; Schema: public; Owner: region2
--

CREATE TABLE region2_votes (
    id integer NOT NULL,
    election_id integer NOT NULL,
    candidate_id integer NOT NULL,
    candidate_count integer
);


ALTER TABLE region2_votes OWNER TO region2;

--
-- TOC entry 2118 (class 0 OID 16809)
-- Dependencies: 185
-- Data for Name: region2_votes; Type: TABLE DATA; Schema: public; Owner: region2
--

COPY region2_votes (id, election_id, candidate_id, candidate_count) FROM stdin;
\.


--
-- TOC entry 2000 (class 2606 OID 16813)
-- Name: region2_votes region1_name_pkey; Type: CONSTRAINT; Schema: public; Owner: region2
--

ALTER TABLE ONLY region2_votes
    ADD CONSTRAINT region1_name_pkey PRIMARY KEY (id);


-- Completed on 2017-02-03 12:28:44

--
-- PostgreSQL database dump complete
--

