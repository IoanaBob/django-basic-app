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
-- Name: admin; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE admin IS 'Main database';


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
-- Name: admin_roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE admin_roles (
    id serial NOT NULL,
    admin_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE admin_roles OWNER TO admin;

--
-- Name: COLUMN admin_roles.admin_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN admin_roles.admin_id IS 'Foreign key reference to admins.id';


--
-- Name: COLUMN admin_roles.role_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN admin_roles.role_id IS 'Foreign key reference to roles.id';


--
-- Name: admins; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE admins (
    id serial NOT NULL,
    first_name character varying(45),
    last_name character varying(45),
    user_name character varying(30),
    password_hash character varying(300),
    email character varying(60)
);


ALTER TABLE admins OWNER TO admin;

--
-- Name: candidates; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE candidates (
   id serial NOT NULL,
    first_name character varying(45),
    last_name character varying(45),
    email character varying(60),
    party_id integer
);


ALTER TABLE candidates OWNER TO admin;

--
-- Name: COLUMN candidates.party_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN candidates.party_id IS 'Foreign key reference to parties.id';


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_site; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO admin;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_site_id_seq OWNER TO admin;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: election_candidates; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE election_candidates (
    id serial NOT NULL,
    election_id integer NOT NULL,
    candidate_id integer NOT NULL
);


ALTER TABLE election_candidates OWNER TO admin;

--
-- Name: COLUMN election_candidates.election_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_candidates.election_id IS 'Foreign key reference to elections.id';


--
-- Name: COLUMN election_candidates.candidate_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_candidates.candidate_id IS 'Foreign key reference to candidates.id';


--
-- Name: election_parties; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE election_parties (
    id serial NOT NULL,
    election_id integer,
    party_id integer
);


ALTER TABLE election_parties OWNER TO admin;

--
-- Name: COLUMN election_parties.election_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_parties.election_id IS 'Foreign key reference to elections.id';


--
-- Name: COLUMN election_parties.party_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_parties.party_id IS 'Foreign key reference to parties.id';


--
-- Name: election_regions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE election_regions (
    id serial NOT NULL,
    election_id integer,
    region_id integer
);


ALTER TABLE election_regions OWNER TO admin;

--
-- Name: elections; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE elections (
    id serial NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    uninominal_voting boolean NOT NULL
);


ALTER TABLE elections OWNER TO admin;

--
-- Name: parties; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE parties (
    id serial NOT NULL,
    name character varying(30)
);


ALTER TABLE parties OWNER TO admin;

--
-- Name: regions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE regions (
    id serial NOT NULL,
    name character varying(60)
);


ALTER TABLE regions OWNER TO admin;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE roles (
    id serial NOT NULL,
    name character varying(45)
);


ALTER TABLE roles OWNER TO admin;

--
-- Name: voter_codes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE voter_codes (
   id serial NOT NULL,
    verified_date timestamp with time zone,
    invalidated_date timestamp with time zone,
    code character varying(15),
    election_id integer,
    region_id integer
);


ALTER TABLE voter_codes OWNER TO admin;

--
-- Name: COLUMN voter_codes.election_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN voter_codes.election_id IS 'Foreign key reference to elections.id';


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Data for Name: admin_roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY admin_roles (id, admin_id, role_id) FROM stdin;
\.


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY admins (id, first_name, last_name, user_name, password_hash, email) FROM stdin;
\.


--
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY candidates (id, first_name, last_name, email, party_id) FROM stdin;
1	Samedited	Mantle	Sam@test.com	\N
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_content_type (id, app_label, model) FROM stdin;
7	admin	logentry
8	auth	test
9	auth	group
10	auth	permission
11	auth	user
12	contenttypes	contenttype
13	sessions	session
14	sites	site
15	voting_system	justchecking
16	voting_system	finalcheck
17	voting_system	test3
18	voting_system	finalcheck2
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('django_content_type_id_seq', 18, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_migrations (id, app, name, applied) FROM stdin;
10	contenttypes	0001_initial	2016-12-14 14:50:33.137273+00
11	auth	0001_initial	2016-12-14 14:50:33.369001+00
12	sites	0001_initial	2016-12-15 14:53:47.644404+00
13	sites	0002_alter_domain_unique	2016-12-15 14:53:47.856303+00
14	voting_system	0001_initial	2016-12-15 15:02:02.335967+00
15	voting_system	0002_justchecking	2016-12-15 15:26:04.973866+00
16	voting_system	0003_finalcheck	2016-12-15 15:34:46.870324+00
17	voting_system	0004_delete_finalcheck	2016-12-15 15:34:47.048021+00
18	voting_system	0005_finalcheck_test3	2016-12-15 15:34:47.264464+00
19	voting_system	0006_finalcheck2	2016-12-15 15:51:35.454411+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('django_migrations_id_seq', 19, true);


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: election_candidates; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY election_candidates (id, election_id, candidate_id) FROM stdin;
\.


--
-- Data for Name: election_parties; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY election_parties (id, election_id, party_id) FROM stdin;
\.


--
-- Data for Name: election_regions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY election_regions (id, election_id, region_id) FROM stdin;
\.


--
-- Data for Name: elections; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY elections (id, start_date, end_date, uninominal_voting) FROM stdin;
\.


--
-- Data for Name: parties; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY parties (id, name) FROM stdin;
\.


--
-- Data for Name: regions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY regions (id, name) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY roles (id, name) FROM stdin;
1	RoleName
\.


--
-- Data for Name: voter_codes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY voter_codes (id, verified_date, invalidated_date, code, election_id, region_id) FROM stdin;
\.


--
-- Name: admins admin_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admins
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- Name: admin_roles admin_roles_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admin_roles
    ADD CONSTRAINT admin_roles_pk PRIMARY KEY (id);


--
-- Name: candidates candidates_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY candidates
    ADD CONSTRAINT candidates_pk PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: election_candidates election_candidates_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_candidates
    ADD CONSTRAINT election_candidates_pk PRIMARY KEY (id);


--
-- Name: election_parties election_parties_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_parties
    ADD CONSTRAINT election_parties_pk PRIMARY KEY (id);


--
-- Name: election_regions election_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_regions
    ADD CONSTRAINT election_regions_pkey PRIMARY KEY (id);


--
-- Name: elections elections_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY elections
    ADD CONSTRAINT elections_pkey PRIMARY KEY (id);


--
-- Name: parties parties_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY parties
    ADD CONSTRAINT parties_pkey PRIMARY KEY (id);


--
-- Name: regions regions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY regions
    ADD CONSTRAINT regions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: voter_codes voter_codes_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY voter_codes
    ADD CONSTRAINT voter_codes_pk PRIMARY KEY (id);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_site_domain_a2e37b91_like ON django_site USING btree (domain varchar_pattern_ops);


--
-- Name: admin_roles admin_roles_admins_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admin_roles
    ADD CONSTRAINT admin_roles_admins_fk FOREIGN KEY (admin_id) REFERENCES admins(id);


--
-- Name: CONSTRAINT admin_roles_admins_fk ON admin_roles; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT admin_roles_admins_fk ON admin_roles IS 'Foreign key to admin table';


--
-- Name: admin_roles admin_roles_roles_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admin_roles
    ADD CONSTRAINT admin_roles_roles_fk FOREIGN KEY (role_id) REFERENCES roles(id) NOT VALID;


--
-- Name: CONSTRAINT admin_roles_roles_fk ON admin_roles; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT admin_roles_roles_fk ON admin_roles IS 'Foreign key to roles table';


--
-- Name: candidates candidates_parties_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY candidates
    ADD CONSTRAINT candidates_parties_fk FOREIGN KEY (party_id) REFERENCES parties(id) NOT VALID;


--
-- Name: CONSTRAINT candidates_parties_fk ON candidates; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT candidates_parties_fk ON candidates IS 'Foreign key to parties table';


--
-- Name: election_candidates election_candidates_candidates_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_candidates
    ADD CONSTRAINT election_candidates_candidates_fk FOREIGN KEY (candidate_id) REFERENCES candidates(id) NOT VALID;


--
-- Name: CONSTRAINT election_candidates_candidates_fk ON election_candidates; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_candidates_candidates_fk ON election_candidates IS 'Foreign key to candidates table';


--
-- Name: election_candidates election_candidates_elections_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_candidates
    ADD CONSTRAINT election_candidates_elections_fk FOREIGN KEY (election_id) REFERENCES elections(id) NOT VALID;


--
-- Name: CONSTRAINT election_candidates_elections_fk ON election_candidates; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_candidates_elections_fk ON election_candidates IS 'Foreign key to elections table';


--
-- Name: election_parties election_parties_elections_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_parties
    ADD CONSTRAINT election_parties_elections_fk FOREIGN KEY (election_id) REFERENCES elections(id) NOT VALID;


--
-- Name: CONSTRAINT election_parties_elections_fk ON election_parties; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_parties_elections_fk ON election_parties IS 'Foreign key to elections table';


--
-- Name: election_parties election_parties_parties; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_parties
    ADD CONSTRAINT election_parties_parties FOREIGN KEY (party_id) REFERENCES parties(id) NOT VALID;


--
-- Name: CONSTRAINT election_parties_parties ON election_parties; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_parties_parties ON election_parties IS 'Foreign key to parties table';


--
-- Name: election_regions fk_election_regions_election_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_regions
    ADD CONSTRAINT fk_election_regions_election_id FOREIGN KEY (election_id) REFERENCES elections(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: election_regions fk_election_regions_region_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_regions
    ADD CONSTRAINT fk_election_regions_region_id FOREIGN KEY (region_id) REFERENCES regions(id);


--
-- Name: voter_codes voter_codes_elections_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY voter_codes
    ADD CONSTRAINT voter_codes_elections_fk FOREIGN KEY (election_id) REFERENCES elections(id) NOT VALID;


--
-- Name: voter_codes voter_codes_regions_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY voter_codes
    ADD CONSTRAINT voter_codes_regions_fk FOREIGN KEY (region_id) REFERENCES regions(id) NOT VALID;


--
-- Name: CONSTRAINT voter_codes_regions_fk ON voter_codes; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT voter_codes_regions_fk ON voter_codes IS 'Foreign Key to regions table';


--
-- PostgreSQL database dump complete
--

