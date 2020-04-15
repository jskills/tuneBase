--
-- Name: artists; Type: TABLE; Schema: goofball; Owner: jskills
--

CREATE TABLE goofball.artists (
    artist_id bigint NOT NULL,
    full_name character varying(200) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    created_date character varying(100),
    last_updated_date character varying(100),
    last_updated_by character varying(20) NOT NULL
);


ALTER TABLE goofball.artists OWNER TO jskills;

--
-- Name: artists_artist_id_seq; Type: SEQUENCE; Schema: goofball; Owner: jskills
--

CREATE SEQUENCE goofball.artists_artist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE goofball.artists_artist_id_seq OWNER TO jskills;

--
-- Name: artists_artist_id_seq; Type: SEQUENCE OWNED BY; Schema: goofball; Owner: jskills
--

ALTER SEQUENCE goofball.artists_artist_id_seq OWNED BY goofball.artists.artist_id;


CREATE TABLE goofball.song_lyrics (
    song_id integer NOT NULL,
    lyrics text NOT NULL,
    created_date timestamp without time zone NOT NULL,
    last_updated_date character varying(100),
    last_updated_by character varying(20) NOT NULL
);


ALTER TABLE goofball.song_lyrics OWNER TO jskills;

--
-- Name: songs; Type: TABLE; Schema: goofball; Owner: jskills
--

CREATE TABLE goofball.songs (
    song_id bigint NOT NULL,
    song_name character varying(250) NOT NULL,
    artist_id integer NOT NULL,
    album character varying(200),
    file_name character varying(100) NOT NULL,
    file_path character varying(300) NOT NULL,
    genre character varying(50) NOT NULL,
    track_number integer,
    year character(4),
    comment character varying(200),
    duration integer,
    bit_rate character varying(20),
    created_date character varying(100),
    last_updated_date character varying(100),
    last_updated_by character varying(20) NOT NULL
);


ALTER TABLE goofball.songs OWNER TO jskills;

--
-- Name: songs_song_id_seq; Type: SEQUENCE; Schema: goofball; Owner: jskills
--

CREATE SEQUENCE goofball.songs_song_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE goofball.songs_song_id_seq OWNER TO jskills;

--
-- Name: songs_song_id_seq; Type: SEQUENCE OWNED BY; Schema: goofball; Owner: jskills
--

ALTER SEQUENCE goofball.songs_song_id_seq OWNED BY goofball.songs.song_id;


CREATE TABLE public.artists (
    artist_id integer NOT NULL,
    full_name character varying(200) NOT NULL,
    first_name character varying(200),
    last_name character varying(200),
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_by character varying(20) NOT NULL
);


ALTER TABLE public.artists OWNER TO jskills;

--
-- Name: artists_artist_id_seq; Type: SEQUENCE; Schema: public; Owner: jskills
--

CREATE SEQUENCE public.artists_artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artists_artist_id_seq OWNER TO jskills;

--
-- Name: artists_artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jskills
--

ALTER SEQUENCE public.artists_artist_id_seq OWNED BY public.artists.artist_id;


--
-- Name: genres; Type: TABLE; Schema: public; Owner: jskills
--

CREATE TABLE public.genres (
    genre_id integer NOT NULL,
    genre_name character varying(100) NOT NULL,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_by character varying(20) NOT NULL
);


ALTER TABLE public.genres OWNER TO jskills;

--
-- Name: genres_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: jskills
--

CREATE SEQUENCE public.genres_genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genres_genre_id_seq OWNER TO jskills;

--
-- Name: genres_genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jskills
--

ALTER SEQUENCE public.genres_genre_id_seq OWNED BY public.genres.genre_id;


--
-- Name: songs; Type: TABLE; Schema: public; Owner: jskills
--

CREATE TABLE public.songs (
    song_id integer NOT NULL,
    song_name character varying(250) NOT NULL,
    artist_id integer NOT NULL,
    album character varying(300) DEFAULT NULL::character varying,
    file_name character varying(100),
    file_path character varying(300) NOT NULL,
    genre character varying(50),
    track_number smallint,
    year character(4) DEFAULT NULL::bpchar,
    comment text,
    duration smallint,
    bit_rate character varying(20) DEFAULT NULL::character varying,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_by character varying(20) NOT NULL,
    genre_id smallint
);


ALTER TABLE public.songs OWNER TO jskills;

--
-- Name: songs_song_id_seq; Type: SEQUENCE; Schema: public; Owner: jskills
--

CREATE SEQUENCE public.songs_song_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.songs_song_id_seq OWNER TO jskills;

--
-- Name: songs_song_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jskills
--

ALTER SEQUENCE public.songs_song_id_seq OWNED BY public.songs.song_id;

