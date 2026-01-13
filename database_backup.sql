--
-- PostgreSQL database dump
--

\restrict i4kmOAgpruuE2JRt5hf3hr82WkpFR8CE26Ne7R6pjgo3x2gXn46DpaSGmhDZOy5

-- Dumped from database version 13.23 (Debian 13.23-1.pgdg13+1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO "user";

--
-- Name: datatype; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.datatype AS ENUM (
    'STRING',
    'INTEGER',
    'FLOAT',
    'DATE',
    'BOOLEAN'
);


ALTER TYPE public.datatype OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: files; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.files (
    id character varying NOT NULL,
    filename character varying NOT NULL,
    spreadsheet_id integer NOT NULL
);


ALTER TABLE public.files OWNER TO "user";

--
-- Name: spreadsheets; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.spreadsheets (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.spreadsheets OWNER TO "user";

--
-- Name: spreadsheets_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.spreadsheets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.spreadsheets_id_seq OWNER TO "user";

--
-- Name: spreadsheets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.spreadsheets_id_seq OWNED BY public.spreadsheets.id;


--
-- Name: validation_rules; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.validation_rules (
    id integer NOT NULL,
    spreadsheet_id integer NOT NULL,
    column_name character varying NOT NULL,
    data_type public.datatype NOT NULL,
    date_format character varying,
    required boolean
);


ALTER TABLE public.validation_rules OWNER TO "user";

--
-- Name: validation_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.validation_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.validation_rules_id_seq OWNER TO "user";

--
-- Name: validation_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.validation_rules_id_seq OWNED BY public.validation_rules.id;


--
-- Name: spreadsheets id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.spreadsheets ALTER COLUMN id SET DEFAULT nextval('public.spreadsheets_id_seq'::regclass);


--
-- Name: validation_rules id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.validation_rules ALTER COLUMN id SET DEFAULT nextval('public.validation_rules_id_seq'::regclass);


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.files (id, filename, spreadsheet_id) FROM stdin;
50e4f6c8-c7f6-458a-8784-f14a2b0cf7ec	planilha1.xlsx	1
\.


--
-- Data for Name: spreadsheets; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.spreadsheets (id, name) FROM stdin;
1	Planilha1
\.


--
-- Data for Name: validation_rules; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.validation_rules (id, spreadsheet_id, column_name, data_type, date_format, required) FROM stdin;
1	1	Nome	STRING		t
2	1	Data de Nacimento	DATE	DD/MM/YYYY	t
3	1	Salário	FLOAT		t
\.


--
-- Name: spreadsheets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.spreadsheets_id_seq', 1, true);


--
-- Name: validation_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.validation_rules_id_seq', 3, true);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: spreadsheets spreadsheets_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.spreadsheets
    ADD CONSTRAINT spreadsheets_pkey PRIMARY KEY (id);


--
-- Name: validation_rules validation_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.validation_rules
    ADD CONSTRAINT validation_rules_pkey PRIMARY KEY (id);


--
-- Name: files files_spreadsheet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_spreadsheet_id_fkey FOREIGN KEY (spreadsheet_id) REFERENCES public.spreadsheets(id);


--
-- Name: validation_rules validation_rules_spreadsheet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.validation_rules
    ADD CONSTRAINT validation_rules_spreadsheet_id_fkey FOREIGN KEY (spreadsheet_id) REFERENCES public.spreadsheets(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: user
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict i4kmOAgpruuE2JRt5hf3hr82WkpFR8CE26Ne7R6pjgo3x2gXn46DpaSGmhDZOy5

