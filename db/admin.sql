--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

-- Started on 2017-02-03 12:27:12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2244 (class 1262 OID 16397)
-- Dependencies: 2243
-- Name: admin; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE admin IS 'Main database';


--
-- TOC entry 1 (class 3079 OID 12387)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2246 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 193 (class 1259 OID 16776)
-- Name: admin_roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE admin_roles (
    id integer NOT NULL,
    admin_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE admin_roles OWNER TO admin;

--
-- TOC entry 2247 (class 0 OID 0)
-- Dependencies: 193
-- Name: COLUMN admin_roles.admin_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN admin_roles.admin_id IS 'Foreign key reference to admins.id';


--
-- TOC entry 2248 (class 0 OID 0)
-- Dependencies: 193
-- Name: COLUMN admin_roles.role_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN admin_roles.role_id IS 'Foreign key reference to roles.id';


--
-- TOC entry 191 (class 1259 OID 16766)
-- Name: admins; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE admins (
    id integer NOT NULL,
    first_name "char",
    last_name "char",
    user_name "char",
    password_hash "char",
    email "char"
);


ALTER TABLE admins OWNER TO admin;

--
-- TOC entry 195 (class 1259 OID 16786)
-- Name: candidates; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE candidates (
    id integer NOT NULL,
    first_name "char",
    last_name "char",
    email "char",
    party_id integer
);


ALTER TABLE candidates OWNER TO admin;

--
-- TOC entry 2249 (class 0 OID 0)
-- Dependencies: 195
-- Name: COLUMN candidates.party_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN candidates.party_id IS 'Foreign key reference to parties.id';


--
-- TOC entry 188 (class 1259 OID 16414)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO admin;

--
-- TOC entry 187 (class 1259 OID 16412)
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
-- TOC entry 2250 (class 0 OID 0)
-- Dependencies: 187
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 186 (class 1259 OID 16403)
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
-- TOC entry 185 (class 1259 OID 16401)
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
-- TOC entry 2251 (class 0 OID 0)
-- Dependencies: 185
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 190 (class 1259 OID 16642)
-- Name: django_site; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO admin;

--
-- TOC entry 189 (class 1259 OID 16640)
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
-- TOC entry 2252 (class 0 OID 0)
-- Dependencies: 189
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- TOC entry 200 (class 1259 OID 16824)
-- Name: election_candidates; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE election_candidates (
    id integer NOT NULL,
    election_id integer NOT NULL,
    candidate_id integer NOT NULL
);


ALTER TABLE election_candidates OWNER TO admin;

--
-- TOC entry 2253 (class 0 OID 0)
-- Dependencies: 200
-- Name: COLUMN election_candidates.election_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_candidates.election_id IS 'Foreign key reference to elections.id';


--
-- TOC entry 2254 (class 0 OID 0)
-- Dependencies: 200
-- Name: COLUMN election_candidates.candidate_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_candidates.candidate_id IS 'Foreign key reference to candidates.id';


--
-- TOC entry 199 (class 1259 OID 16819)
-- Name: election_parties; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE election_parties (
    id integer NOT NULL,
    election_id integer,
    party_id integer
);


ALTER TABLE election_parties OWNER TO admin;

--
-- TOC entry 2255 (class 0 OID 0)
-- Dependencies: 199
-- Name: COLUMN election_parties.election_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_parties.election_id IS 'Foreign key reference to elections.id';


--
-- TOC entry 2256 (class 0 OID 0)
-- Dependencies: 199
-- Name: COLUMN election_parties.party_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN election_parties.party_id IS 'Foreign key reference to parties.id';


--
-- TOC entry 201 (class 1259 OID 16874)
-- Name: election_regions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE election_regions (
    id integer NOT NULL,
    election_id integer,
    region_id integer
);


ALTER TABLE election_regions OWNER TO admin;

--
-- TOC entry 196 (class 1259 OID 16791)
-- Name: elections; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE elections (
    id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    uninominal_voting boolean NOT NULL
);


ALTER TABLE elections OWNER TO admin;

--
-- TOC entry 194 (class 1259 OID 16781)
-- Name: parties; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE parties (
    id integer NOT NULL,
    name "char"
);


ALTER TABLE parties OWNER TO admin;

--
-- TOC entry 198 (class 1259 OID 16801)
-- Name: regions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE regions (
    id integer NOT NULL,
    name "char"
);


ALTER TABLE regions OWNER TO admin;

--
-- TOC entry 192 (class 1259 OID 16771)
-- Name: roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE roles (
    id integer NOT NULL,
    name "char"
);


ALTER TABLE roles OWNER TO admin;

--
-- TOC entry 197 (class 1259 OID 16796)
-- Name: voter_codes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE voter_codes (
    id integer NOT NULL,
    verified_date timestamp with time zone,
    invalidated_date timestamp with time zone,
    code "char",
    election_id integer,
    region_id integer
);


ALTER TABLE voter_codes OWNER TO admin;

--
-- TOC entry 2257 (class 0 OID 0)
-- Dependencies: 197
-- Name: COLUMN voter_codes.election_id; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN voter_codes.election_id IS 'Foreign key reference to elections.id';


--
-- TOC entry 2059 (class 2604 OID 16417)
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 2058 (class 2604 OID 16406)
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 2060 (class 2604 OID 16645)
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- TOC entry 2230 (class 0 OID 16776)
-- Dependencies: 193
-- Data for Name: admin_roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY admin_roles (id, admin_id, role_id) FROM stdin;
\.


--
-- TOC entry 2228 (class 0 OID 16766)
-- Dependencies: 191
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY admins (id, first_name, last_name, user_name, password_hash, email) FROM stdin;
\.


--
-- TOC entry 2232 (class 0 OID 16786)
-- Dependencies: 195
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY candidates (id, first_name, last_name, email, party_id) FROM stdin;
\.


--
-- TOC entry 2225 (class 0 OID 16414)
-- Dependencies: 188
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
-- TOC entry 2258 (class 0 OID 0)
-- Dependencies: 187
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('django_content_type_id_seq', 18, true);


--
-- TOC entry 2223 (class 0 OID 16403)
-- Dependencies: 186
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_migrations (id, app, name, applied) FROM stdin;
10	contenttypes	0001_initial	2016-12-14 16:50:33.137273+02
11	auth	0001_initial	2016-12-14 16:50:33.369001+02
12	sites	0001_initial	2016-12-15 16:53:47.644404+02
13	sites	0002_alter_domain_unique	2016-12-15 16:53:47.856303+02
14	voting_system	0001_initial	2016-12-15 17:02:02.335967+02
15	voting_system	0002_justchecking	2016-12-15 17:26:04.973866+02
16	voting_system	0003_finalcheck	2016-12-15 17:34:46.870324+02
17	voting_system	0004_delete_finalcheck	2016-12-15 17:34:47.048021+02
18	voting_system	0005_finalcheck_test3	2016-12-15 17:34:47.264464+02
19	voting_system	0006_finalcheck2	2016-12-15 17:51:35.454411+02
\.


--
-- TOC entry 2259 (class 0 OID 0)
-- Dependencies: 185
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('django_migrations_id_seq', 19, true);


--
-- TOC entry 2227 (class 0 OID 16642)
-- Dependencies: 190
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- TOC entry 2260 (class 0 OID 0)
-- Dependencies: 189
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- TOC entry 2237 (class 0 OID 16824)
-- Dependencies: 200
-- Data for Name: election_candidates; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY election_candidates (id, election_id, candidate_id) FROM stdin;
\.


--
-- TOC entry 2236 (class 0 OID 16819)
-- Dependencies: 199
-- Data for Name: election_parties; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY election_parties (id, election_id, party_id) FROM stdin;
\.


--
-- TOC entry 2238 (class 0 OID 16874)
-- Dependencies: 201
-- Data for Name: election_regions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY election_regions (id, election_id, region_id) FROM stdin;
\.


--
-- TOC entry 2233 (class 0 OID 16791)
-- Dependencies: 196
-- Data for Name: elections; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY elections (id, start_date, end_date, uninominal_voting) FROM stdin;
\.


--
-- TOC entry 2231 (class 0 OID 16781)
-- Dependencies: 194
-- Data for Name: parties; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY parties (id, name) FROM stdin;
\.


--
-- TOC entry 2235 (class 0 OID 16801)
-- Dependencies: 198
-- Data for Name: regions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY regions (id, name) FROM stdin;
\.


--
-- TOC entry 2229 (class 0 OID 16771)
-- Dependencies: 192
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY roles (id, name) FROM stdin;
\.


--
-- TOC entry 2234 (class 0 OID 16796)
-- Dependencies: 197
-- Data for Name: voter_codes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY voter_codes (id, verified_date, invalidated_date, code, election_id, region_id) FROM stdin;
\.


--
-- TOC entry 2073 (class 2606 OID 16770)
-- Name: admins admin_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admins
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- TOC entry 2077 (class 2606 OID 16780)
-- Name: admin_roles admin_roles_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admin_roles
    ADD CONSTRAINT admin_roles_pk PRIMARY KEY (id);


--
-- TOC entry 2081 (class 2606 OID 16790)
-- Name: candidates candidates_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY candidates
    ADD CONSTRAINT candidates_pk PRIMARY KEY (id);


--
-- TOC entry 2064 (class 2606 OID 16421)
-- Name: django_content_type django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 2066 (class 2606 OID 16419)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2062 (class 2606 OID 16411)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 2069 (class 2606 OID 16649)
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- TOC entry 2071 (class 2606 OID 16647)
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- TOC entry 2091 (class 2606 OID 16828)
-- Name: election_candidates election_candidates_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_candidates
    ADD CONSTRAINT election_candidates_pk PRIMARY KEY (id);


--
-- TOC entry 2089 (class 2606 OID 16823)
-- Name: election_parties election_parties_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_parties
    ADD CONSTRAINT election_parties_pk PRIMARY KEY (id);


--
-- TOC entry 2093 (class 2606 OID 16878)
-- Name: election_regions election_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_regions
    ADD CONSTRAINT election_regions_pkey PRIMARY KEY (id);


--
-- TOC entry 2083 (class 2606 OID 16795)
-- Name: elections elections_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY elections
    ADD CONSTRAINT elections_pkey PRIMARY KEY (id);


--
-- TOC entry 2079 (class 2606 OID 16785)
-- Name: parties parties_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY parties
    ADD CONSTRAINT parties_pkey PRIMARY KEY (id);


--
-- TOC entry 2087 (class 2606 OID 16805)
-- Name: regions regions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY regions
    ADD CONSTRAINT regions_pkey PRIMARY KEY (id);


--
-- TOC entry 2075 (class 2606 OID 16775)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 2085 (class 2606 OID 16800)
-- Name: voter_codes voter_codes_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY voter_codes
    ADD CONSTRAINT voter_codes_pk PRIMARY KEY (id);


--
-- TOC entry 2067 (class 1259 OID 16650)
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_site_domain_a2e37b91_like ON django_site USING btree (domain varchar_pattern_ops);


--
-- TOC entry 2095 (class 2606 OID 16829)
-- Name: admin_roles admin_roles_admins_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admin_roles
    ADD CONSTRAINT admin_roles_admins_fk FOREIGN KEY (admin_id) REFERENCES admins(id);


--
-- TOC entry 2261 (class 0 OID 0)
-- Dependencies: 2095
-- Name: CONSTRAINT admin_roles_admins_fk ON admin_roles; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT admin_roles_admins_fk ON admin_roles IS 'Foreign key to admin table';


--
-- TOC entry 2094 (class 2606 OID 16834)
-- Name: admin_roles admin_roles_roles_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY admin_roles
    ADD CONSTRAINT admin_roles_roles_fk FOREIGN KEY (role_id) REFERENCES roles(id) NOT VALID;


--
-- TOC entry 2262 (class 0 OID 0)
-- Dependencies: 2094
-- Name: CONSTRAINT admin_roles_roles_fk ON admin_roles; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT admin_roles_roles_fk ON admin_roles IS 'Foreign key to roles table';


--
-- TOC entry 2096 (class 2606 OID 16859)
-- Name: candidates candidates_parties_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY candidates
    ADD CONSTRAINT candidates_parties_fk FOREIGN KEY (party_id) REFERENCES parties(id) NOT VALID;


--
-- TOC entry 2263 (class 0 OID 0)
-- Dependencies: 2096
-- Name: CONSTRAINT candidates_parties_fk ON candidates; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT candidates_parties_fk ON candidates IS 'Foreign key to parties table';


--
-- TOC entry 2102 (class 2606 OID 16844)
-- Name: election_candidates election_candidates_candidates_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_candidates
    ADD CONSTRAINT election_candidates_candidates_fk FOREIGN KEY (candidate_id) REFERENCES candidates(id) NOT VALID;


--
-- TOC entry 2264 (class 0 OID 0)
-- Dependencies: 2102
-- Name: CONSTRAINT election_candidates_candidates_fk ON election_candidates; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_candidates_candidates_fk ON election_candidates IS 'Foreign key to candidates table';


--
-- TOC entry 2101 (class 2606 OID 16839)
-- Name: election_candidates election_candidates_elections_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_candidates
    ADD CONSTRAINT election_candidates_elections_fk FOREIGN KEY (election_id) REFERENCES elections(id) NOT VALID;


--
-- TOC entry 2265 (class 0 OID 0)
-- Dependencies: 2101
-- Name: CONSTRAINT election_candidates_elections_fk ON election_candidates; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_candidates_elections_fk ON election_candidates IS 'Foreign key to elections table';


--
-- TOC entry 2099 (class 2606 OID 16849)
-- Name: election_parties election_parties_elections_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_parties
    ADD CONSTRAINT election_parties_elections_fk FOREIGN KEY (election_id) REFERENCES elections(id) NOT VALID;


--
-- TOC entry 2266 (class 0 OID 0)
-- Dependencies: 2099
-- Name: CONSTRAINT election_parties_elections_fk ON election_parties; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_parties_elections_fk ON election_parties IS 'Foreign key to elections table';


--
-- TOC entry 2100 (class 2606 OID 16854)
-- Name: election_parties election_parties_parties; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_parties
    ADD CONSTRAINT election_parties_parties FOREIGN KEY (party_id) REFERENCES parties(id) NOT VALID;


--
-- TOC entry 2267 (class 0 OID 0)
-- Dependencies: 2100
-- Name: CONSTRAINT election_parties_parties ON election_parties; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT election_parties_parties ON election_parties IS 'Foreign key to parties table';


--
-- TOC entry 2103 (class 2606 OID 16879)
-- Name: election_regions fk_election_regions_election_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_regions
    ADD CONSTRAINT fk_election_regions_election_id FOREIGN KEY (election_id) REFERENCES elections(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- TOC entry 2104 (class 2606 OID 16884)
-- Name: election_regions fk_election_regions_region_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY election_regions
    ADD CONSTRAINT fk_election_regions_region_id FOREIGN KEY (region_id) REFERENCES regions(id);


--
-- TOC entry 2097 (class 2606 OID 16864)
-- Name: voter_codes voter_codes_elections_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY voter_codes
    ADD CONSTRAINT voter_codes_elections_fk FOREIGN KEY (election_id) REFERENCES elections(id) NOT VALID;


--
-- TOC entry 2098 (class 2606 OID 16869)
-- Name: voter_codes voter_codes_regions_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY voter_codes
    ADD CONSTRAINT voter_codes_regions_fk FOREIGN KEY (region_id) REFERENCES regions(id) NOT VALID;


--
-- TOC entry 2268 (class 0 OID 0)
-- Dependencies: 2098
-- Name: CONSTRAINT voter_codes_regions_fk ON voter_codes; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON CONSTRAINT voter_codes_regions_fk ON voter_codes IS 'Foreign Key to regions table';


-- Completed on 2017-02-03 12:27:12

--
-- PostgreSQL database dump complete
--

