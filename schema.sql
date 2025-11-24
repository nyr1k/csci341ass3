--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: addresses; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.addresses (
    a_member_id integer,
    a_house_number integer,
    a_street character varying(32),
    a_town character varying(32)
);


ALTER TABLE public.addresses OWNER TO nyrik;

--
-- Name: appointments; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.appointments (
    appointment_id integer NOT NULL,
    ap_caregiver_id integer,
    ap_member_id integer,
    ap_date date,
    ap_time time without time zone,
    ap_work_hours numeric(4,2),
    ap_status character varying(20)
);


ALTER TABLE public.appointments OWNER TO nyrik;

--
-- Name: caregivers; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.caregivers (
    caregiver_id integer NOT NULL,
    c_photo text,
    c_gender character varying(10),
    c_care_type character varying(30),
    c_hourly_rate numeric(10,2),
    CONSTRAINT caregivers_c_care_type_check CHECK (((c_care_type)::text = ANY ((ARRAY['babysitter'::character varying, 'elder'::character varying, 'playmate'::character varying])::text[]))),
    CONSTRAINT caregivers_c_gender_check CHECK (((c_gender)::text = ANY ((ARRAY['male'::character varying, 'female'::character varying, 'other'::character varying])::text[]))),
    CONSTRAINT caregivers_c_hourly_rate_check CHECK ((c_hourly_rate > 0.0))
);


ALTER TABLE public.caregivers OWNER TO nyrik;

--
-- Name: job_applications; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.job_applications (
    ja_caregiver_id integer NOT NULL,
    ja_job_id integer NOT NULL,
    ja_date_applied date
);


ALTER TABLE public.job_applications OWNER TO nyrik;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.jobs (
    job_id integer NOT NULL,
    j_member_id integer,
    j_care_type character varying(20),
    j_reqs text,
    j_date_post date,
    CONSTRAINT jobs_j_care_type_check CHECK (((j_care_type)::text = ANY ((ARRAY['babysitter'::character varying, 'elder'::character varying, 'playmate'::character varying])::text[])))
);


ALTER TABLE public.jobs OWNER TO nyrik;

--
-- Name: members; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.members (
    member_id integer NOT NULL,
    m_house_rules text,
    m_depend_descr text
);


ALTER TABLE public.members OWNER TO nyrik;

--
-- Name: users; Type: TABLE; Schema: public; Owner: nyrik
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    u_email character varying(32),
    u_name character varying(32),
    u_surname character varying(32),
    u_city character varying(32),
    u_phone_number character varying(20),
    u_profile_descr text,
    u_password character varying(15)
);


ALTER TABLE public.users OWNER TO nyrik;

--
-- Data for Name: addresses; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.addresses (a_member_id, a_house_number, a_street, a_town) FROM stdin;
\.


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.appointments (appointment_id, ap_caregiver_id, ap_member_id, ap_date, ap_time, ap_work_hours, ap_status) FROM stdin;
\.


--
-- Data for Name: caregivers; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.caregivers (caregiver_id, c_photo, c_gender, c_care_type, c_hourly_rate) FROM stdin;
\.


--
-- Data for Name: job_applications; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.job_applications (ja_caregiver_id, ja_job_id, ja_date_applied) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.jobs (job_id, j_member_id, j_care_type, j_reqs, j_date_post) FROM stdin;
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.members (member_id, m_house_rules, m_depend_descr) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: nyrik
--

COPY public.users (user_id, u_email, u_name, u_surname, u_city, u_phone_number, u_profile_descr, u_password) FROM stdin;
\.


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (appointment_id);


--
-- Name: caregivers caregivers_pkey; Type: CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_pkey PRIMARY KEY (caregiver_id);


--
-- Name: job_applications job_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_pkey PRIMARY KEY (ja_caregiver_id, ja_job_id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (job_id);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (member_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: addresses addresses_a_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_a_member_id_fkey FOREIGN KEY (a_member_id) REFERENCES public.members(member_id) ON DELETE CASCADE;


--
-- Name: appointments appointments_ap_caregiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_ap_caregiver_id_fkey FOREIGN KEY (ap_caregiver_id) REFERENCES public.caregivers(caregiver_id) ON DELETE CASCADE;


--
-- Name: appointments appointments_ap_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_ap_member_id_fkey FOREIGN KEY (ap_member_id) REFERENCES public.members(member_id) ON DELETE CASCADE;


--
-- Name: caregivers caregivers_caregiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_caregiver_id_fkey FOREIGN KEY (caregiver_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: job_applications job_applications_ja_caregiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_ja_caregiver_id_fkey FOREIGN KEY (ja_caregiver_id) REFERENCES public.caregivers(caregiver_id) ON DELETE CASCADE;


--
-- Name: job_applications job_applications_ja_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_ja_job_id_fkey FOREIGN KEY (ja_job_id) REFERENCES public.jobs(job_id) ON DELETE CASCADE;


--
-- Name: jobs jobs_j_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_j_member_id_fkey FOREIGN KEY (j_member_id) REFERENCES public.members(member_id) ON DELETE CASCADE;


--
-- Name: members members_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nyrik
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

