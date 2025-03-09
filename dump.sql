--
-- PostgreSQL database dump
--

-- Dumped from database version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.1)

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
-- Name: newsmail; Type: SCHEMA; Schema: -; Owner: marco
--

CREATE SCHEMA newsmail;


ALTER SCHEMA newsmail OWNER TO marco;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appuser; Type: TABLE; Schema: newsmail; Owner: marco
--

CREATE TABLE newsmail.appuser (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying,
    pub_key character varying,
    firstname character varying,
    lastname character varying,
    is_active boolean NOT NULL
);


ALTER TABLE newsmail.appuser OWNER TO marco;

--
-- Name: appuser_id_seq; Type: SEQUENCE; Schema: newsmail; Owner: marco
--

CREATE SEQUENCE newsmail.appuser_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE newsmail.appuser_id_seq OWNER TO marco;

--
-- Name: appuser_id_seq; Type: SEQUENCE OWNED BY; Schema: newsmail; Owner: marco
--

ALTER SEQUENCE newsmail.appuser_id_seq OWNED BY newsmail.appuser.id;


--
-- Name: cansendon; Type: TABLE; Schema: newsmail; Owner: marco
--

CREATE TABLE newsmail.cansendon (
    id integer NOT NULL,
    channel integer NOT NULL,
    appuser integer NOT NULL
);


ALTER TABLE newsmail.cansendon OWNER TO marco;

--
-- Name: cansendon_id_seq; Type: SEQUENCE; Schema: newsmail; Owner: marco
--

CREATE SEQUENCE newsmail.cansendon_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE newsmail.cansendon_id_seq OWNER TO marco;

--
-- Name: cansendon_id_seq; Type: SEQUENCE OWNED BY; Schema: newsmail; Owner: marco
--

ALTER SEQUENCE newsmail.cansendon_id_seq OWNED BY newsmail.cansendon.id;


--
-- Name: channel; Type: TABLE; Schema: newsmail; Owner: marco
--

CREATE TABLE newsmail.channel (
    code integer NOT NULL,
    name character varying(30) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    owner integer NOT NULL
);


ALTER TABLE newsmail.channel OWNER TO marco;

--
-- Name: channel_code_seq; Type: SEQUENCE; Schema: newsmail; Owner: marco
--

CREATE SEQUENCE newsmail.channel_code_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE newsmail.channel_code_seq OWNER TO marco;

--
-- Name: channel_code_seq; Type: SEQUENCE OWNED BY; Schema: newsmail; Owner: marco
--

ALTER SEQUENCE newsmail.channel_code_seq OWNED BY newsmail.channel.code;


--
-- Name: newsmail; Type: TABLE; Schema: newsmail; Owner: marco
--

CREATE TABLE newsmail.newsmail (
    msgid character(64) NOT NULL,
    sender integer NOT NULL,
    title character varying(100) NOT NULL,
    body text,
    htmlbody text,
    statuscode smallint DEFAULT 0 NOT NULL,
    creation_date timestamp without time zone,
    expiration_date timestamp without time zone
);


ALTER TABLE newsmail.newsmail OWNER TO marco;

--
-- Name: senton; Type: TABLE; Schema: newsmail; Owner: marco
--

CREATE TABLE newsmail.senton (
    id integer NOT NULL,
    newsmail character(64) NOT NULL,
    channel integer NOT NULL,
    enable boolean NOT NULL
);


ALTER TABLE newsmail.senton OWNER TO marco;

--
-- Name: senton_id_seq; Type: SEQUENCE; Schema: newsmail; Owner: marco
--

CREATE SEQUENCE newsmail.senton_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE newsmail.senton_id_seq OWNER TO marco;

--
-- Name: senton_id_seq; Type: SEQUENCE OWNED BY; Schema: newsmail; Owner: marco
--

ALTER SEQUENCE newsmail.senton_id_seq OWNED BY newsmail.senton.id;


--
-- Name: appuser id; Type: DEFAULT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.appuser ALTER COLUMN id SET DEFAULT nextval('newsmail.appuser_id_seq'::regclass);


--
-- Name: cansendon id; Type: DEFAULT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.cansendon ALTER COLUMN id SET DEFAULT nextval('newsmail.cansendon_id_seq'::regclass);


--
-- Name: channel code; Type: DEFAULT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.channel ALTER COLUMN code SET DEFAULT nextval('newsmail.channel_code_seq'::regclass);


--
-- Name: senton id; Type: DEFAULT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.senton ALTER COLUMN id SET DEFAULT nextval('newsmail.senton_id_seq'::regclass);


--
-- Name: appuser appuser_pkey; Type: CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.appuser
    ADD CONSTRAINT appuser_pkey PRIMARY KEY (id);


--
-- Name: cansendon cansendon_pkey; Type: CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.cansendon
    ADD CONSTRAINT cansendon_pkey PRIMARY KEY (id);


--
-- Name: channel channel_pkey; Type: CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.channel
    ADD CONSTRAINT channel_pkey PRIMARY KEY (code);


--
-- Name: newsmail newsmail_pkey; Type: CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.newsmail
    ADD CONSTRAINT newsmail_pkey PRIMARY KEY (msgid);


--
-- Name: senton senton_pkey; Type: CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.senton
    ADD CONSTRAINT senton_pkey PRIMARY KEY (id);


--
-- Name: cansendon cansendon_appuser_fkey; Type: FK CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.cansendon
    ADD CONSTRAINT cansendon_appuser_fkey FOREIGN KEY (appuser) REFERENCES newsmail.appuser(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cansendon cansendon_channel_fkey; Type: FK CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.cansendon
    ADD CONSTRAINT cansendon_channel_fkey FOREIGN KEY (channel) REFERENCES newsmail.channel(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: channel channel_owner_fkey; Type: FK CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.channel
    ADD CONSTRAINT channel_owner_fkey FOREIGN KEY (owner) REFERENCES newsmail.appuser(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: newsmail newsmail_sender_fkey; Type: FK CONSTRAINT; Schema: newsmail; Owner: marco
--

ALTER TABLE ONLY newsmail.newsmail
    ADD CONSTRAINT newsmail_sender_fkey FOREIGN KEY (sender) REFERENCES newsmail.appuser(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

