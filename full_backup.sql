--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

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
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(100),
    profile_pic character varying(255)
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: admin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admin_id_seq OWNER TO postgres;

--
-- Name: admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admin_id_seq OWNED BY public.admin.id;


--
-- Name: business_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.business_categories (
    id integer NOT NULL,
    business_id integer,
    category_id integer
);


ALTER TABLE public.business_categories OWNER TO postgres;

--
-- Name: business_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.business_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.business_categories_id_seq OWNER TO postgres;

--
-- Name: business_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.business_categories_id_seq OWNED BY public.business_categories.id;


--
-- Name: business_registration_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.business_registration_requests (
    id integer NOT NULL,
    business_name character varying(100) NOT NULL,
    shop_no character varying(100) NOT NULL,
    phone_number character varying(20),
    description text NOT NULL,
    processed boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    user_id integer,
    category character varying(50) NOT NULL,
    block_num character varying(50),
    email character varying(100)
);


ALTER TABLE public.business_registration_requests OWNER TO postgres;

--
-- Name: business_registration_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.business_registration_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.business_registration_requests_id_seq OWNER TO postgres;

--
-- Name: business_registration_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.business_registration_requests_id_seq OWNED BY public.business_registration_requests.id;


--
-- Name: businesses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.businesses (
    id integer NOT NULL,
    owner_id integer,
    business_name character varying(100) NOT NULL,
    shop_no character varying(100) NOT NULL,
    phone_number character varying(20) NOT NULL,
    description text NOT NULL,
    is_subscribed boolean DEFAULT false,
    media_type character varying(10),
    media_url text,
    block_num character varying(50),
    email character varying(100),
    category character varying(100),
    CONSTRAINT businesses_media_type_check CHECK (((media_type)::text = ANY ((ARRAY['image'::character varying, 'video'::character varying])::text[])))
);


ALTER TABLE public.businesses OWNER TO postgres;

--
-- Name: businesses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.businesses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.businesses_id_seq OWNER TO postgres;

--
-- Name: businesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.businesses_id_seq OWNED BY public.businesses.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    category_name character varying(255) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: claim_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.claim_requests (
    id integer NOT NULL,
    business_id integer,
    user_id integer,
    phone_number character varying(255),
    email character varying(255),
    category character varying(255),
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    reviewed boolean DEFAULT false
);


ALTER TABLE public.claim_requests OWNER TO postgres;

--
-- Name: claim_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.claim_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.claim_requests_id_seq OWNER TO postgres;

--
-- Name: claim_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.claim_requests_id_seq OWNED BY public.claim_requests.id;


--
-- Name: images_videos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images_videos (
    id integer NOT NULL,
    business_id integer,
    media_type character varying(10),
    media_url text NOT NULL,
    CONSTRAINT images_videos_media_type_check CHECK (((media_type)::text = ANY ((ARRAY['image'::character varying, 'video'::character varying])::text[])))
);


ALTER TABLE public.images_videos OWNER TO postgres;

--
-- Name: images_videos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.images_videos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.images_videos_id_seq OWNER TO postgres;

--
-- Name: images_videos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.images_videos_id_seq OWNED BY public.images_videos.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    subscription_id integer,
    payment_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    amount numeric(10,2) NOT NULL,
    payment_status character varying(20),
    payment_method character varying(50),
    CONSTRAINT payments_payment_status_check CHECK (((payment_status)::text = ANY ((ARRAY['pending'::character varying, 'completed'::character varying])::text[])))
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO postgres;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: subscription_plans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription_plans (
    id integer NOT NULL,
    plan_name character varying(50) NOT NULL,
    amount numeric(10,2) NOT NULL,
    duration integer NOT NULL
);


ALTER TABLE public.subscription_plans OWNER TO postgres;

--
-- Name: subscription_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_plans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscription_plans_id_seq OWNER TO postgres;

--
-- Name: subscription_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_plans_id_seq OWNED BY public.subscription_plans.id;


--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscriptions (
    id integer NOT NULL,
    business_id integer,
    subscription_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(20),
    plan_id integer,
    CONSTRAINT subscriptions_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'confirmed'::character varying])::text[])))
);


ALTER TABLE public.subscriptions OWNER TO postgres;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscriptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscriptions_id_seq OWNER TO postgres;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscriptions_id_seq OWNED BY public.subscriptions.id;


--
-- Name: user_registration_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_registration_requests (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password text NOT NULL,
    email character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    processed boolean DEFAULT false,
    name character varying(250),
    phone character varying(250)
);


ALTER TABLE public.user_registration_requests OWNER TO postgres;

--
-- Name: user_registration_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_registration_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_registration_requests_id_seq OWNER TO postgres;

--
-- Name: user_registration_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_registration_requests_id_seq OWNED BY public.user_registration_requests.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    is_admin boolean DEFAULT false,
    is_approved boolean DEFAULT false,
    profile_image text,
    suspended boolean DEFAULT false,
    activation_token text,
    is_activated boolean DEFAULT false,
    registration_request_id integer,
    name character varying(255),
    phone character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: admin id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin ALTER COLUMN id SET DEFAULT nextval('public.admin_id_seq'::regclass);


--
-- Name: business_categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_categories ALTER COLUMN id SET DEFAULT nextval('public.business_categories_id_seq'::regclass);


--
-- Name: business_registration_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_registration_requests ALTER COLUMN id SET DEFAULT nextval('public.business_registration_requests_id_seq'::regclass);


--
-- Name: businesses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.businesses ALTER COLUMN id SET DEFAULT nextval('public.businesses_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: claim_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.claim_requests ALTER COLUMN id SET DEFAULT nextval('public.claim_requests_id_seq'::regclass);


--
-- Name: images_videos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images_videos ALTER COLUMN id SET DEFAULT nextval('public.images_videos_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: subscription_plans id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans ALTER COLUMN id SET DEFAULT nextval('public.subscription_plans_id_seq'::regclass);


--
-- Name: subscriptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions ALTER COLUMN id SET DEFAULT nextval('public.subscriptions_id_seq'::regclass);


--
-- Name: user_registration_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_requests ALTER COLUMN id SET DEFAULT nextval('public.user_registration_requests_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin (id, username, password, email, profile_pic) FROM stdin;
1	admin3	pbkdf2:sha256:600000$tdZtGRrCZtN8k8vp$07dbd014566415cfa16ec986310d750198d041bbc8580ee10bc9facf6fae5181	admin@efe.com3	static/uploads/IMG-20210815-WA0036.jpg
\.


--
-- Data for Name: business_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.business_categories (id, business_id, category_id) FROM stdin;
16	17	4
19	48	15
20	50	4
21	54	16
26	10	3
27	55	18
29	57	12
31	59	18
32	63	4
33	65	5
34	66	4
\.


--
-- Data for Name: business_registration_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.business_registration_requests (id, business_name, shop_no, phone_number, description, processed, created_at, user_id, category, block_num, email) FROM stdin;
11	R-pro Group	1	08058470559	Hello Peoples	t	2024-08-12 10:04:37.781882	1	Education	block A	support@rprotravels.com
18	Charity Organization	12	08058470559	help the poor	t	2024-08-13 15:13:09.452017	1	Food	block B	support@rprotravels.com
19	R-pro	23	08058470559	the	t	2024-08-21 18:22:45.977883	1	Fashion	block B	ajirip45@gmail.com
21	DM Laundry	78	08058470559	laundary services	t	2024-08-29 09:48:52.933137	1	Health	block B	info-abroad@rprotravels.com
23	SIMPLY LOVELY LAUNDRY & FASHIONS	39&40	0802 592 2093	Fashion And Laundry Services	t	2024-08-29 10:55:17.587472	6	Fashion	Block F4	laundryandfashion@gmail.com
24	R-pro Consult	3	08058470559	stydy abroad	t	2024-08-29 13:49:11.827905	8	Education	block a	info-abroad@rprotravels.com
27	Lagos Help	3	08058470559	eat well	f	2024-08-29 13:57:15.100875	8	Health	block D	admin@efe.com
25	Business Consult	22	08058470559	grow in business and Charity	t	2024-08-29 13:55:17.550847	8	Food	block c	support@rprotravels.com
26	Business Consult	22	08058470559	grow in business and Charity	t	2024-08-29 13:55:17.601669	8	Food	block c	support@rprotravels.com
\.


--
-- Data for Name: businesses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.businesses (id, owner_id, business_name, shop_no, phone_number, description, is_subscribed, media_type, media_url, block_num, email, category) FROM stdin;
49	\N	ADBIRT SOFTWARE COMPANY	2358	000-000-0000	Default description	f	\N	\N	BLOCK A1	hpfbusinesses@gmail.com	Uncategorized
51	\N	360 DEGREES LOGISTICS	1438	000-000-0000	Default description	f	\N	\N	BLOCK E1	hpfbusinesses@gmail.com	Uncategorized
52	\N	A & B & C	2614	000-000-0000	Default description	f	\N	\N	BLOCK A2	hpfbusinesses@gmail.com	Uncategorized
53	\N	ABBYS LANDROMART	1361	000-000-0000	Default description	f	\N	\N	BLOCK E1	hpfbusinesses@gmail.com	Uncategorized
66	8	Business Consult	22	08058470559	grow in business and Charity	t	image	static/uploads/effizy-Logo.png	block c	support@rprotravels.com	Food
17	1	Charity Organization	12	08058470559	help the poor	f	\N	\N	block B	support@rprotravels.com	Food
48	1	ABBYS LANDROMART	1361	08058470559	we do laundry to entertain	t	image	static/uploads/IMG-20210829-WA0007.jpg	BLOCK E1	info-abroad@rprotravels.com	Entertainment
10	1	R-pro Group	255	08058470559	Hello Peoples Of God	t	video	static/uploads/VID-20210916-WA0017.mp4	block A	support@rprotravels.com	GYM
55	\N	R-pro	23	08058470559	the	f	\N	\N	block B	ajirip45@gmail.com	Fashion
57	1	DM Laundry	78	08058470559	laundary services	f	\N	\N	block B	info-abroad@rprotravels.com	Health
50	1	TILES SHOP	916	08058470559	helping he poor	t	video	static/uploads/VID-20210901-WA0014.mp4	BLOCK D1	support@rprotravels.com	Food
54	1	ADBIRT SOFTWARE COMPANY	2358	08058470559	oiuyfdtrduikihoiuhiugjj	t	video	static/uploads/VID-20211119-WA0033.mp4	BLOCK A1	support@rprotravels.com	Real Estate
60	\N	WISDOM GROUP	1832	000-000-0000	Default description	f	\N	\N	BLOCK F4	hpfbusinesses@gmail.com	Uncategorized
61	\N	WISTERIA ESTATES LTD	2462	000-000-0000	Default description	f	\N	\N	BLOCK A1	hpfbusinesses@gmail.com	Uncategorized
62	\N	WOODLAND PROPERTIES	1831	000-000-0000	Default description	f	\N	\N	BLOCK F4	hpfbusinesses@gmail.com	Uncategorized
64	\N	WORTHWHILE VENTURES	1831	000-000-0000	Default description	f	\N	\N	BLOCK F4	hpfbusinesses@gmail.com	Uncategorized
59	6	SIMPLY LOVELY LAUNDRY & FASHIONS	39&40	0802 592 2093	Fashion And Laundry Services	t	image	static/uploads/lovely.png	Block F4	laundryandfashion@gmail.com	Fashion
63	6	WORLD CLASS LIMITED	2944	08058470559	help the poop	t	\N	\N	BLOCK A4	cyjustwebsolution@gmail.com	Food
65	8	R-pro Consult	3	08058470559	stydy abroad	f	\N	\N	block a	info-abroad@rprotravels.com	Education
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, category_name) FROM stdin;
2	Tech
3	GYM
4	Food
5	Education
12	Health
13	Automobile
15	Entertainment
16	Real Estate
17	Travels
18	Fashion
\.


--
-- Data for Name: claim_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.claim_requests (id, business_id, user_id, phone_number, email, category, description, created_at, reviewed) FROM stdin;
20	48	1	08058470559	info-abroad@rprotravels.com	Entertainment	we do laundry to entertain	2024-08-19 20:06:46.200722	t
21	50	1	08058470559	support@rprotravels.com	Food	helping he poor	2024-08-20 15:30:58.220138	t
22	54	1	08058470559	support@rprotravels.com	Real Estate	oiuyfdtrduikihoiuhiugjj	2024-08-21 14:19:41.716804	t
23	53	1	08058470559	info-abroad@rprotravels.com	Tech	abroad	2024-08-21 18:42:31.724353	f
24	63	6	08058470559	cyjustwebsolution@gmail.com	Food	help the poop	2024-08-29 12:24:24.756148	t
\.


--
-- Data for Name: images_videos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images_videos (id, business_id, media_type, media_url) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, subscription_id, payment_date, amount, payment_status, payment_method) FROM stdin;
\.


--
-- Data for Name: subscription_plans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscription_plans (id, plan_name, amount, duration) FROM stdin;
1	Monthly	10000.00	1
2	Yearly	85000.00	12
\.


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscriptions (id, business_id, subscription_date, status, plan_id) FROM stdin;
4	10	2024-08-12 10:07:14.91707	confirmed	1
16	48	2024-08-19 20:07:26.109624	confirmed	1
17	50	2024-08-20 15:31:47.174816	confirmed	1
18	54	2024-08-21 14:34:40.532853	confirmed	2
20	59	2024-08-29 10:56:36.214424	confirmed	2
21	63	2024-08-29 12:28:55.327594	confirmed	2
22	66	2024-08-29 14:09:36.671394	confirmed	1
\.


--
-- Data for Name: user_registration_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_registration_requests (id, username, password, email, created_at, processed, name, phone) FROM stdin;
1	Ajiri	pbkdf2:sha256:600000$lfBNNCHYypBfCgVw$f43c6df66bb1189ea9c59208464604df852b94d968a60662ccdcb9dc7ba3073a	ajirip45@gmail.com	2024-08-09 10:42:48.556007	t	\N	\N
13	r-pro	pbkdf2:sha256:600000$I4XZ1ktx2nLqVIUt$a7bc95a452825b8fcea511b55a9f6ff772ae3b540734283fe0561a78b8f49501	rprogroupcrm@gmail.com	2024-08-24 17:42:57.304243	t	R-pro Group	08075951947
15	Cyjust	pbkdf2:sha256:600000$RnN3cOTsTrmmPYh8$faeacd06ed0874ea24c1707070a4e46f28e2ba0d164464989fc548ba36527fe1	cyjustwebsolution@gmail.com	2024-08-29 13:46:54.714616	t	Cyjust Engineer	08075951947
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password, is_admin, is_approved, profile_image, suspended, activation_token, is_activated, registration_request_id, name, phone) FROM stdin;
8	Cyjust	cyjustwebsolution@gmail.com	pbkdf2:sha256:600000$RnN3cOTsTrmmPYh8$faeacd06ed0874ea24c1707070a4e46f28e2ba0d164464989fc548ba36527fe1	f	t	./static/uploads\\IMG-20210903-WA0013.jpg	f	ImN5anVzdHdlYnNvbHV0aW9uQGdtYWlsLmNvbSI.ZtBt1A.D9-Xkdse8Er17EYMsJx6YZUHqqM	t	15	Cyjust Engineer	08075951947
1	Ajiri Oghene	ajirip45@gmail.com	pbkdf2:sha256:600000$cWmB1QJzRy8v8r1f$fdb272d48e8e7306217e75be001837f0152f86916e9372cef1ce2d0ef8df1a24	f	t	./static/uploads\\lovely.png	f	ImFqaXJpcDQ1QGdtYWlsLmNvbSI.ZrXk4w.w1NnmrJmDyCrO2XJACZGbKAZScs	t	1	\N	\N
6	Lovely	rprogroupcrm@gmail.com	pbkdf2:sha256:600000$LnIB0jZ2CKDMtMz9$2fad647645fca88a0dca36da249f12babcde2bab1c6228c9fbd84f470a96f5e3	f	t	./static/uploads\\lovely.png	f	InJwcm9ncm91cGNybUBnbWFpbC5jb20i.ZsoORg.X-EhowaH94irn6FSXIrDmqmD-C8	t	13	R-pro Group	08075951947
\.


--
-- Name: admin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admin_id_seq', 1, true);


--
-- Name: business_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.business_categories_id_seq', 34, true);


--
-- Name: business_registration_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.business_registration_requests_id_seq', 27, true);


--
-- Name: businesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.businesses_id_seq', 66, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 18, true);


--
-- Name: claim_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.claim_requests_id_seq', 24, true);


--
-- Name: images_videos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.images_videos_id_seq', 1, false);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: subscription_plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_plans_id_seq', 2312, true);


--
-- Name: subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscriptions_id_seq', 22, true);


--
-- Name: user_registration_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_registration_requests_id_seq', 15, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- Name: admin admin_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_username_key UNIQUE (username);


--
-- Name: business_categories business_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_categories
    ADD CONSTRAINT business_categories_pkey PRIMARY KEY (id);


--
-- Name: business_registration_requests business_registration_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_registration_requests
    ADD CONSTRAINT business_registration_requests_pkey PRIMARY KEY (id);


--
-- Name: businesses businesses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.businesses
    ADD CONSTRAINT businesses_pkey PRIMARY KEY (id);


--
-- Name: categories categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_category_name_key UNIQUE (category_name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: claim_requests claim_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.claim_requests
    ADD CONSTRAINT claim_requests_pkey PRIMARY KEY (id);


--
-- Name: images_videos images_videos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images_videos
    ADD CONSTRAINT images_videos_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: subscription_plans subscription_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans
    ADD CONSTRAINT subscription_plans_pkey PRIMARY KEY (id);


--
-- Name: subscription_plans subscription_plans_plan_name_duration_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans
    ADD CONSTRAINT subscription_plans_plan_name_duration_key UNIQUE (plan_name, duration);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: business_categories unique_business_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_categories
    ADD CONSTRAINT unique_business_category UNIQUE (business_id, category_id);


--
-- Name: user_registration_requests user_registration_requests_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_requests
    ADD CONSTRAINT user_registration_requests_email_key UNIQUE (email);


--
-- Name: user_registration_requests user_registration_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_requests
    ADD CONSTRAINT user_registration_requests_pkey PRIMARY KEY (id);


--
-- Name: user_registration_requests user_registration_requests_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_requests
    ADD CONSTRAINT user_registration_requests_username_key UNIQUE (username);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: business_categories business_categories_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_categories
    ADD CONSTRAINT business_categories_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: business_categories business_categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_categories
    ADD CONSTRAINT business_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: business_registration_requests business_registration_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.business_registration_requests
    ADD CONSTRAINT business_registration_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: businesses businesses_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.businesses
    ADD CONSTRAINT businesses_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: claim_requests claim_requests_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.claim_requests
    ADD CONSTRAINT claim_requests_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: claim_requests claim_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.claim_requests
    ADD CONSTRAINT claim_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users fk_users_registration_request; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_registration_request FOREIGN KEY (registration_request_id) REFERENCES public.user_registration_requests(id) ON DELETE CASCADE;


--
-- Name: images_videos images_videos_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images_videos
    ADD CONSTRAINT images_videos_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id);


--
-- Name: payments payments_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id) ON DELETE CASCADE;


--
-- Name: subscriptions subscriptions_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.businesses(id) ON DELETE CASCADE;


--
-- Name: subscriptions subscriptions_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.subscription_plans(id);


--
-- Name: users users_registration_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_registration_request_id_fkey FOREIGN KEY (registration_request_id) REFERENCES public.user_registration_requests(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

