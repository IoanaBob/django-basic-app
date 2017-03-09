--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

-- Started on 2017-02-03 12:29:46

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
-- TOC entry 2131 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 185 (class 1259 OID 16758)
-- Name: auth_test; Type: TABLE; Schema: public; Owner: voterauth
--

CREATE TABLE auth_test (
    "ID" integer NOT NULL,
    name text
);


ALTER TABLE auth_test OWNER TO voterauth;

--
-- TOC entry 186 (class 1259 OID 16806)
-- Name: voter_auth; Type: TABLE; Schema: public; Owner: voterauth
--

CREATE TABLE voter_auth (
    id integer,
    voter_code_number integer,
    password_hash "char"
);


ALTER TABLE voter_auth OWNER TO voterauth;

--
-- TOC entry 2123 (class 0 OID 16758)
-- Dependencies: 185
-- Data for Name: auth_test; Type: TABLE DATA; Schema: public; Owner: voterauth
--

COPY auth_test ("ID", name) FROM stdin;
1	mytest
2	hey how are you
3	rvd fxn
4	hi
\.


--
-- TOC entry 2124 (class 0 OID 16806)
-- Dependencies: 186
-- Data for Name: voter_auth; Type: TABLE DATA; Schema: public; Owner: voterauth
--

COPY voter_auth (id, voter_code_number, password_hash) FROM stdin;
\.


--
-- TOC entry 2005 (class 2606 OID 16765)
-- Name: auth_test auth_test_pkey; Type: CONSTRAINT; Schema: public; Owner: voterauth
--

ALTER TABLE ONLY auth_test
    ADD CONSTRAINT auth_test_pkey PRIMARY KEY ("ID");


-- Completed on 2017-02-03 12:29:47

--
-- PostgreSQL database dump complete
--

