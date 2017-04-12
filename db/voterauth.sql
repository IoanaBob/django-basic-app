--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_test; Type: TABLE; Schema: public; Owner: voterauth
--

CREATE TABLE auth_test (
    "ID" integer NOT NULL,
    name text
);


ALTER TABLE auth_test OWNER TO voterauth;

--
-- Name: voter_auth; Type: TABLE; Schema: public; Owner: voterauth
--

CREATE TABLE voter_auth (
    id integer,
    voter_code_number integer,
    password_hash character varying(300)
);


ALTER TABLE voter_auth OWNER TO voterauth;

--
-- Data for Name: auth_test; Type: TABLE DATA; Schema: public; Owner: voterauth
--

COPY auth_test ("ID", name) FROM stdin;
1	mytest
2	hey how are you
3	rvd fxn
4	hi
5	SamTest
\.


--
-- Data for Name: voter_auth; Type: TABLE DATA; Schema: public; Owner: voterauth
--

COPY voter_auth (id, voter_code_number, password_hash) FROM stdin;
\.


--
-- Name: auth_test auth_test_pkey; Type: CONSTRAINT; Schema: public; Owner: voterauth
--

ALTER TABLE ONLY auth_test
    ADD CONSTRAINT auth_test_pkey PRIMARY KEY ("ID");


--
-- PostgreSQL database dump complete
--

