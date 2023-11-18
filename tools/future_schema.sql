PGDMP         )    
        
    {            wapadb     15.5 (Ubuntu 15.5-1.pgdg22.04+1)     15.4 (Ubuntu 15.4-2.pgdg22.04+1) F               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16388    wapadb    DATABASE     r   CREATE DATABASE wapadb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE wapadb;
                postgres    false                       0    0    DATABASE wapadb    ACL     �   GRANT CONNECT ON DATABASE wapadb TO warp;
GRANT CONNECT ON DATABASE wapadb TO transnode2;
GRANT CONNECT ON DATABASE wapadb TO teledummy;
GRANT CONNECT ON DATABASE wapadb TO ata;
GRANT CONNECT ON DATABASE wapadb TO windmill;
                   postgres    false    4357                        2615    917444    future    SCHEMA        CREATE SCHEMA future;
    DROP SCHEMA future;
                postgres    false                       0    0    SCHEMA future    ACL     %   GRANT USAGE ON SCHEMA future TO ata;
                   postgres    false    16            �            1259    917610    ua_district_hromadas    TABLE     �   CREATE TABLE future.ua_district_hromadas (
    id integer NOT NULL,
    name_uk text,
    longcode text,
    district_id integer
);
 (   DROP TABLE future.ua_district_hromadas;
       future         heap    postgres    false    16                       0    0    TABLE ua_district_hromadas    COMMENT     �   COMMENT ON TABLE future.ua_district_hromadas IS 'List of territorial units of Ukraine (level 3 of the post-reform administrative structure)';
          future          postgres    false    232            �            1259    917615    ua_localities    TABLE     A  CREATE TABLE future.ua_localities (
    id integer NOT NULL,
    name_uk text,
    longcode text,
    type_id integer,
    name_ru text,
    index1 integer,
    index2 integer,
    latitude character varying,
    longitude character varying,
    indexcoatsu character varying,
    name_en text,
    hromada_id integer
);
 !   DROP TABLE future.ua_localities;
       future         heap    postgres    false    16            	           0    0    TABLE ua_localities    COMMENT     ^  COMMENT ON TABLE future.ua_localities IS 'List of localities of Ukraine (level 4 of the post-reform administration structure).
Main table of the locality sub-cluster. Most of the data is taken from https://zakon.rada.gov.ua/rada/show/v0290914-20#Text (the most recent version of the list dated December 16, 2021). Whenever possible locations were matched against the Nova Poshta database (it uses the old administrative system and doesn''t have the occupied localities), from which lat, lon, indexes and russian versions of names were taken. Approximately 2/3 of all localities (~19K/29K) were resolved.';
          future          postgres    false    233            
           0    0    COLUMN ua_localities.name_uk    COMMENT     `   COMMENT ON COLUMN future.ua_localities.name_uk IS 'Symbol U+2019 (’) is used for apostrophe';
          future          postgres    false    233                       0    0    COLUMN ua_localities.name_en    COMMENT     �   COMMENT ON COLUMN future.ua_localities.name_en IS 'English version is derived by transliterating the Ukrainian version of the name (custom script based on the National Standard https://en.wikipedia.org/wiki/Romanization_of_Ukrainian)';
          future          postgres    false    233            �            1259    917620    ua_locality_types    TABLE     h   CREATE TABLE future.ua_locality_types (
    id integer NOT NULL,
    description text,
    code text
);
 %   DROP TABLE future.ua_locality_types;
       future         heap    postgres    false    16                       0    0    TABLE ua_locality_types    COMMENT     Q   COMMENT ON TABLE future.ua_locality_types IS 'ENUM of Ukrainian locality types';
          future          postgres    false    234            �            1259    917625 
   ua_regions    TABLE     |   CREATE TABLE future.ua_regions (
    id integer NOT NULL,
    name_uk text NOT NULL,
    longcode text,
    name_ru text
);
    DROP TABLE future.ua_regions;
       future         heap    postgres    false    16                       0    0    TABLE ua_regions    COMMENT     z   COMMENT ON TABLE future.ua_regions IS 'List of regions of Ukraine (level 1 of the post-reform administration structure)';
          future          postgres    false    235            �            1259    917630    ua_regions_districts    TABLE     �   CREATE TABLE future.ua_regions_districts (
    id integer NOT NULL,
    name_uk text,
    longcode text,
    region_id integer
);
 (   DROP TABLE future.ua_regions_districts;
       future         heap    postgres    false    16                       0    0    TABLE ua_regions_districts    COMMENT     �   COMMENT ON TABLE future.ua_regions_districts IS 'List of districts within regions of Ukraine (level 2 of the post-reform administration structure)';
          future          postgres    false    236            �            1259    917635    localities_by_region    VIEW     ,  CREATE VIEW future.localities_by_region AS
 SELECT lo.name_uk AS locality,
    lo.longcode,
    hro.name_uk AS hromada,
    dist.name_uk AS district,
    reg.name_uk AS region,
    loc_types.description AS type
   FROM ((((future.ua_localities lo
     LEFT JOIN future.ua_district_hromadas hro ON ((lo.hromada_id = hro.id)))
     LEFT JOIN future.ua_regions_districts dist ON ((hro.district_id = dist.id)))
     LEFT JOIN future.ua_regions reg ON ((dist.region_id = reg.id)))
     JOIN future.ua_locality_types loc_types ON ((lo.type_id = loc_types.id)));
 '   DROP VIEW future.localities_by_region;
       future          postgres    false    233    235    235    234    234    233    233    233    232    232    232    236    236    236    16            �           1255    917640    get_region_localities(text)    FUNCTION     �   CREATE FUNCTION future.get_region_localities(region text) RETURNS SETOF future.localities_by_region
    LANGUAGE sql
    AS $$
select * from localities_by_region lbr
where lbr.region = region;
$$;
 9   DROP FUNCTION future.get_region_localities(region text);
       future          postgres    false    16    237                       1259    917945    e_mash_mapdata    TABLE     }   CREATE TABLE future.e_mash_mapdata (
    id bigint NOT NULL,
    captured text[],
    hotspots jsonb[],
    day_id bigint
);
 "   DROP TABLE future.e_mash_mapdata;
       future         heap    postgres    false    16                       0    0    TABLE e_mash_mapdata    COMMENT     q   COMMENT ON TABLE future.e_mash_mapdata IS 'Data obtained from the Mash-produced interactive map of hostilities';
          future          postgres    false    282                       1259    917950    e_mash_mapdata_id_seq    SEQUENCE     �   ALTER TABLE future.e_mash_mapdata ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.e_mash_mapdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    282    16                       1259    917951    localitylevel1regions_id_seq    SEQUENCE     �   ALTER TABLE future.ua_regions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.localitylevel1regions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    235                       1259    917952    localitylevel2districts_id_seq    SEQUENCE     �   ALTER TABLE future.ua_regions_districts ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.localitylevel2districts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    236    16                       1259    917953 %   localitylevel3territorialunits_id_seq    SEQUENCE     �   ALTER TABLE future.ua_district_hromadas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.localitylevel3territorialunits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    232                       1259    917954    localitylevel4localities_id_seq    SEQUENCE     �   ALTER TABLE future.ua_localities ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.localitylevel4localities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    233                        1259    917955    ua_localities_districts    TABLE     �   CREATE TABLE future.ua_localities_districts (
    id integer NOT NULL,
    name_uk text,
    longcode text,
    locality_id integer
);
 +   DROP TABLE future.ua_localities_districts;
       future         heap    postgres    false    16                       0    0    TABLE ua_localities_districts    COMMENT     �   COMMENT ON TABLE future.ua_localities_districts IS 'List of districts within larger cities of Ukraine (level 5 of the post-reform administration structure)';
          future          postgres    false    288            !           1259    917960 &   localitylevel5localitydisrticts_id_seq    SEQUENCE     �   ALTER TABLE future.ua_localities_districts ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.localitylevel5localitydisrticts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    288            "           1259    917961    localitytypes_id_seq    SEQUENCE     �   ALTER TABLE future.ua_locality_types ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.localitytypes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    234            #           1259    917962    meduza_dow_stream    TABLE       CREATE TABLE future.meduza_dow_stream (
    id bigint NOT NULL,
    dow_id bigint NOT NULL,
    published_at timestamp without time zone,
    blocks jsonb[],
    important boolean,
    meduza_id bigint,
    created_at timestamp with time zone DEFAULT now()
);
 %   DROP TABLE future.meduza_dow_stream;
       future         heap    postgres    false    16            $           1259    917968    meduza_dow_stream_id_seq    SEQUENCE     �   ALTER TABLE future.meduza_dow_stream ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.meduza_dow_stream_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    291            %           1259    917969    modrf_briefings    TABLE     �   CREATE TABLE future.modrf_briefings (
    id integer NOT NULL,
    seq_number integer,
    text text,
    date date,
    w json,
    localities json,
    text_m text
);
 #   DROP TABLE future.modrf_briefings;
       future         heap    postgres    false    16                       0    0    TABLE modrf_briefings    COMMENT     �  COMMENT ON TABLE future.modrf_briefings IS 'Table contains full texts and dates of the RF Mnistry of Defence regular briefings on the state of the war. For dates between February 24 and March 12 texts are obtained by transcribing the videos; for dates between March 12 and April 7? 2 versions of the text are available, one obtained through transcription, second - from the MoD''s official Telegram channel. After April 7, only the telegram-version is available.
Columns "localities" and "w" contain derivative data about localities and weapons respectively, which is obtained by reducing the corresponding briefing''s text.
Column "localities" list of ids of villages/towns/cities mentioned in a briefing from the ukraine_localities table.
Colum "w" is a json structure with numbers of claimed victories. Structure is based on the same template and uses the same designation, but each contains only a portion of keys.';
          future          postgres    false    293            &           1259    917974    modrf_briefings_id_seq    SEQUENCE     �   ALTER TABLE future.modrf_briefings ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.modrf_briefings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    293    16            '           1259    917975    rf_territorial    TABLE     �   CREATE TABLE future.rf_territorial (
    id bigint NOT NULL,
    name text,
    region_type text,
    wiki_ref text,
    name_en text
);
 "   DROP TABLE future.rf_territorial;
       future         heap    postgres    false    16                       0    0    TABLE rf_territorial    COMMENT     Y   COMMENT ON TABLE future.rf_territorial IS 'Highest level of RF administrative division';
          future          postgres    false    295            (           1259    917980    rf_territorial_id_seq    SEQUENCE     �   ALTER TABLE future.rf_territorial ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.rf_territorial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    295            )           1259    917981    rodniki    TABLE     �  CREATE TABLE future.rodniki (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    type text,
    title text,
    author text,
    date date,
    url text,
    description text,
    tags text,
    photo text,
    author_origin_id integer,
    have boolean DEFAULT false NOT NULL,
    duration integer,
    url_is_alive boolean DEFAULT true NOT NULL,
    available boolean DEFAULT true NOT NULL
);
    DROP TABLE future.rodniki;
       future         heap    postgres    false    16                       0    0    COLUMN rodniki.available    COMMENT     O   COMMENT ON COLUMN future.rodniki.available IS 'False if can''t be downloaded';
          future          postgres    false    297            *           1259    917990    rodniki_id_seq    SEQUENCE     �   ALTER TABLE future.rodniki ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.rodniki_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    297            +           1259    917991    tryvoga_alerts    TABLE     �   CREATE TABLE future.tryvoga_alerts (
    id integer NOT NULL,
    day_date timestamp without time zone,
    type boolean,
    localities jsonb
);
 "   DROP TABLE future.tryvoga_alerts;
       future         heap    postgres    false    16            ,           1259    917996    tryvoga_alerts_id_seq    SEQUENCE     �   ALTER TABLE future.tryvoga_alerts ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME future.tryvoga_alerts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            future          postgres    false    16    299            M           2606    1833527 *   e_mash_mapdata e_mash_mapdata_day_date_key 
   CONSTRAINT     g   ALTER TABLE ONLY future.e_mash_mapdata
    ADD CONSTRAINT e_mash_mapdata_day_date_key UNIQUE (day_id);
 T   ALTER TABLE ONLY future.e_mash_mapdata DROP CONSTRAINT e_mash_mapdata_day_date_key;
       future            postgres    false    282            O           2606    1833529 "   e_mash_mapdata e_mash_mapdata_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY future.e_mash_mapdata
    ADD CONSTRAINT e_mash_mapdata_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY future.e_mash_mapdata DROP CONSTRAINT e_mash_mapdata_pkey;
       future            postgres    false    282            I           2606    1833810 %   ua_regions localitylevel1regions_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY future.ua_regions
    ADD CONSTRAINT localitylevel1regions_pkey PRIMARY KEY (id);
 O   ALTER TABLE ONLY future.ua_regions DROP CONSTRAINT localitylevel1regions_pkey;
       future            postgres    false    235            K           2606    1833812 1   ua_regions_districts localitylevel2districts_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY future.ua_regions_districts
    ADD CONSTRAINT localitylevel2districts_pkey PRIMARY KEY (id);
 [   ALTER TABLE ONLY future.ua_regions_districts DROP CONSTRAINT localitylevel2districts_pkey;
       future            postgres    false    236            C           2606    1833802 8   ua_district_hromadas localitylevel3territorialunits_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY future.ua_district_hromadas
    ADD CONSTRAINT localitylevel3territorialunits_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY future.ua_district_hromadas DROP CONSTRAINT localitylevel3territorialunits_pkey;
       future            postgres    false    232            E           2606    1833804 +   ua_localities localitylevel4localities_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY future.ua_localities
    ADD CONSTRAINT localitylevel4localities_pkey PRIMARY KEY (id);
 U   ALTER TABLE ONLY future.ua_localities DROP CONSTRAINT localitylevel4localities_pkey;
       future            postgres    false    233            Q           2606    1833806 <   ua_localities_districts localitylevel5localitydisrticts_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY future.ua_localities_districts
    ADD CONSTRAINT localitylevel5localitydisrticts_pkey PRIMARY KEY (id);
 f   ALTER TABLE ONLY future.ua_localities_districts DROP CONSTRAINT localitylevel5localitydisrticts_pkey;
       future            postgres    false    288            G           2606    1833808 $   ua_locality_types localitytypes_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY future.ua_locality_types
    ADD CONSTRAINT localitytypes_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY future.ua_locality_types DROP CONSTRAINT localitytypes_pkey;
       future            postgres    false    234            S           2606    1833588 (   meduza_dow_stream meduza_dow_stream_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY future.meduza_dow_stream
    ADD CONSTRAINT meduza_dow_stream_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY future.meduza_dow_stream DROP CONSTRAINT meduza_dow_stream_pkey;
       future            postgres    false    291            U           2606    1833608 $   modrf_briefings modrf_briefings_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY future.modrf_briefings
    ADD CONSTRAINT modrf_briefings_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY future.modrf_briefings DROP CONSTRAINT modrf_briefings_pkey;
       future            postgres    false    293            W           2606    1833694 )   rf_territorial rf_territorial_name_en_key 
   CONSTRAINT     g   ALTER TABLE ONLY future.rf_territorial
    ADD CONSTRAINT rf_territorial_name_en_key UNIQUE (name_en);
 S   ALTER TABLE ONLY future.rf_territorial DROP CONSTRAINT rf_territorial_name_en_key;
       future            postgres    false    295            Y           2606    1833696 &   rf_territorial rf_territorial_name_key 
   CONSTRAINT     a   ALTER TABLE ONLY future.rf_territorial
    ADD CONSTRAINT rf_territorial_name_key UNIQUE (name);
 P   ALTER TABLE ONLY future.rf_territorial DROP CONSTRAINT rf_territorial_name_key;
       future            postgres    false    295            [           2606    1833698 "   rf_territorial rf_territorial_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY future.rf_territorial
    ADD CONSTRAINT rf_territorial_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY future.rf_territorial DROP CONSTRAINT rf_territorial_pkey;
       future            postgres    false    295            ]           2606    1833700 *   rf_territorial rf_territorial_wiki_ref_key 
   CONSTRAINT     i   ALTER TABLE ONLY future.rf_territorial
    ADD CONSTRAINT rf_territorial_wiki_ref_key UNIQUE (wiki_ref);
 T   ALTER TABLE ONLY future.rf_territorial DROP CONSTRAINT rf_territorial_wiki_ref_key;
       future            postgres    false    295            _           2606    1833702    rodniki rodniki_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY future.rodniki
    ADD CONSTRAINT rodniki_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY future.rodniki DROP CONSTRAINT rodniki_pkey;
       future            postgres    false    297            a           2606    1833800 "   tryvoga_alerts tryvoga_alerts_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY future.tryvoga_alerts
    ADD CONSTRAINT tryvoga_alerts_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY future.tryvoga_alerts DROP CONSTRAINT tryvoga_alerts_pkey;
       future            postgres    false    299            f           2606    1833895 )   e_mash_mapdata e_mash_mapdata_day_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.e_mash_mapdata
    ADD CONSTRAINT e_mash_mapdata_day_id_fkey FOREIGN KEY (day_id) REFERENCES public.days_of_war(id);
 S   ALTER TABLE ONLY future.e_mash_mapdata DROP CONSTRAINT e_mash_mapdata_day_id_fkey;
       future          postgres    false    282            h           2606    1833950 /   meduza_dow_stream meduza_dow_stream_dow_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.meduza_dow_stream
    ADD CONSTRAINT meduza_dow_stream_dow_id_fkey FOREIGN KEY (dow_id) REFERENCES public.days_of_war(id);
 Y   ALTER TABLE ONLY future.meduza_dow_stream DROP CONSTRAINT meduza_dow_stream_dow_id_fkey;
       future          postgres    false    291            b           2606    1834300 :   ua_district_hromadas ua_district_hromadas_district_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.ua_district_hromadas
    ADD CONSTRAINT ua_district_hromadas_district_id_fkey FOREIGN KEY (district_id) REFERENCES future.ua_regions_districts(id);
 d   ALTER TABLE ONLY future.ua_district_hromadas DROP CONSTRAINT ua_district_hromadas_district_id_fkey;
       future          postgres    false    232    4171    236            g           2606    1834315 @   ua_localities_districts ua_localities_districts_locality_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.ua_localities_districts
    ADD CONSTRAINT ua_localities_districts_locality_id_fkey FOREIGN KEY (locality_id) REFERENCES future.ua_localities(id);
 j   ALTER TABLE ONLY future.ua_localities_districts DROP CONSTRAINT ua_localities_districts_locality_id_fkey;
       future          postgres    false    233    4165    288            c           2606    1834305 +   ua_localities ua_localities_hromada_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.ua_localities
    ADD CONSTRAINT ua_localities_hromada_id_fkey FOREIGN KEY (hromada_id) REFERENCES future.ua_district_hromadas(id);
 U   ALTER TABLE ONLY future.ua_localities DROP CONSTRAINT ua_localities_hromada_id_fkey;
       future          postgres    false    232    233    4163            d           2606    1834310 (   ua_localities ua_localities_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.ua_localities
    ADD CONSTRAINT ua_localities_type_id_fkey FOREIGN KEY (type_id) REFERENCES future.ua_locality_types(id);
 R   ALTER TABLE ONLY future.ua_localities DROP CONSTRAINT ua_localities_type_id_fkey;
       future          postgres    false    234    233    4167            e           2606    1834320 8   ua_regions_districts ua_regions_districts_region_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY future.ua_regions_districts
    ADD CONSTRAINT ua_regions_districts_region_id_fkey FOREIGN KEY (region_id) REFERENCES future.ua_regions(id);
 b   ALTER TABLE ONLY future.ua_regions_districts DROP CONSTRAINT ua_regions_districts_region_id_fkey;
       future          postgres    false    4169    235    236            �           0    917962    meduza_dow_stream    ROW SECURITY     ?   ALTER TABLE future.meduza_dow_stream ENABLE ROW LEVEL SECURITY;          future          postgres    false    291            �           3256    919266    rodniki read_rodniki    POLICY     F   CREATE POLICY read_rodniki ON future.rodniki FOR SELECT USING (true);
 ,   DROP POLICY read_rodniki ON future.rodniki;
       future          postgres    false    297           