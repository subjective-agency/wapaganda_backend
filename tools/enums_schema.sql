PGDMP     5    (    
        
    {            wapadb     15.5 (Ubuntu 15.5-1.pgdg22.04+1)     15.4 (Ubuntu 15.4-2.pgdg22.04+1) -    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16388    wapadb    DATABASE     r   CREATE DATABASE wapadb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE wapadb;
                postgres    false            �           0    0    DATABASE wapadb    ACL     �   GRANT CONNECT ON DATABASE wapadb TO warp;
GRANT CONNECT ON DATABASE wapadb TO transnode2;
GRANT CONNECT ON DATABASE wapadb TO teledummy;
GRANT CONNECT ON DATABASE wapadb TO ata;
GRANT CONNECT ON DATABASE wapadb TO windmill;
                   postgres    false    4345                        2615    917442    enums    SCHEMA        CREATE SCHEMA enums;
    DROP SCHEMA enums;
                postgres    false            �           0    0    SCHEMA enums    ACL     $   GRANT USAGE ON SCHEMA enums TO ata;
                   postgres    false    17            
           1259    917885    bundle_types    TABLE     �   CREATE TABLE enums.bundle_types (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    code text,
    description text
);
    DROP TABLE enums.bundle_types;
       enums         heap    postgres    false    17                       1259    917892    bundle_types_id_seq    SEQUENCE     �   ALTER TABLE enums.bundle_types ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.bundle_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    266    17                       1259    917893    isco08_index    TABLE     �   CREATE TABLE enums.isco08_index (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    isco08 bigint,
    name_en text,
    name_ru text,
    name_uk text,
    appended boolean
);
    DROP TABLE enums.isco08_index;
       enums         heap    postgres    false    17            �           0    0    COLUMN isco08_index.appended    COMMENT     q   COMMENT ON COLUMN enums.isco08_index.appended IS 'If true, the term is a custom addition to the original index';
          enums          postgres    false    268                       1259    917903    isco08_index_id_seq    SEQUENCE     �   ALTER TABLE enums.isco08_index ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.isco08_index_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    268    17                       1259    917904    isco08_taxonomy    TABLE     .  CREATE TABLE enums.isco08_taxonomy (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    term text,
    isco_code text,
    definition text,
    tasks_include text,
    included_occupations text,
    excluded_occupations text,
    notes text,
    skill_level smallint
);
 "   DROP TABLE enums.isco08_taxonomy;
       enums         heap    postgres    false    17                       1259    917910    isco08_taxonomy_closure    TABLE     m   CREATE TABLE enums.isco08_taxonomy_closure (
    ancestor bigint NOT NULL,
    descendant bigint NOT NULL
);
 *   DROP TABLE enums.isco08_taxonomy_closure;
       enums         heap    postgres    false    17                       1259    917913    isco08_taxonomy_id_seq    SEQUENCE     �   ALTER TABLE enums.isco08_taxonomy ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.isco08_taxonomy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    270    17                       1259    917914    orgs_taxonomy    TABLE     �   CREATE TABLE enums.orgs_taxonomy (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    term text,
    code text,
    definition text,
    notes text
);
     DROP TABLE enums.orgs_taxonomy;
       enums         heap    postgres    false    17                       1259    917920    orgs_taxonomy_closure    TABLE     k   CREATE TABLE enums.orgs_taxonomy_closure (
    ancestor bigint NOT NULL,
    descendant bigint NOT NULL
);
 (   DROP TABLE enums.orgs_taxonomy_closure;
       enums         heap    postgres    false    17                       1259    917923    orgs_taxonomy_id_seq    SEQUENCE     �   ALTER TABLE enums.orgs_taxonomy ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.orgs_taxonomy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    17    273                       1259    917924    rucr_taxonomy    TABLE       CREATE TABLE enums.rucr_taxonomy (
    id bigint NOT NULL,
    content_en text,
    content_ru text,
    content_uk text,
    tags text[],
    xml_id text,
    xml_data jsonb,
    updated_on timestamp with time zone,
    status text,
    is_core boolean DEFAULT false NOT NULL
);
     DROP TABLE enums.rucr_taxonomy;
       enums         heap    postgres    false    17                       1259    917930    rucr_taxonomy_id_seq    SEQUENCE     �   ALTER TABLE enums.rucr_taxonomy ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.rucr_taxonomy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    276    17                       1259    917931    theory_types    TABLE     �   CREATE TABLE enums.theory_types (
    id bigint NOT NULL,
    term text,
    description text,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);
    DROP TABLE enums.theory_types;
       enums         heap    postgres    false    17                       1259    917937    theory_types_id_seq    SEQUENCE     �   ALTER TABLE enums.theory_types ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.theory_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    17    278                       1259    917938    transfactory_nodes    TABLE     �   CREATE TABLE enums.transfactory_nodes (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    node_name text,
    status text,
    whisper_base_args text[]
);
 %   DROP TABLE enums.transfactory_nodes;
       enums         heap    postgres    false    17                       1259    917944    transfactory_nodes_id_seq    SEQUENCE     �   ALTER TABLE enums.transfactory_nodes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME enums.transfactory_nodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            enums          postgres    false    280    17            A           2606    1833504    bundle_types bundle_types_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY enums.bundle_types
    ADD CONSTRAINT bundle_types_pkey PRIMARY KEY (id);
 G   ALTER TABLE ONLY enums.bundle_types DROP CONSTRAINT bundle_types_pkey;
       enums            postgres    false    266            C           2606    1833549    isco08_index isco08_index_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY enums.isco08_index
    ADD CONSTRAINT isco08_index_pkey PRIMARY KEY (id);
 G   ALTER TABLE ONLY enums.isco08_index DROP CONSTRAINT isco08_index_pkey;
       enums            postgres    false    268            G           2606    1833553 4   isco08_taxonomy_closure isco08_taxonomy_closure_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY enums.isco08_taxonomy_closure
    ADD CONSTRAINT isco08_taxonomy_closure_pkey PRIMARY KEY (ancestor, descendant);
 ]   ALTER TABLE ONLY enums.isco08_taxonomy_closure DROP CONSTRAINT isco08_taxonomy_closure_pkey;
       enums            postgres    false    271    271            E           2606    1833551 $   isco08_taxonomy isco08_taxonomy_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY enums.isco08_taxonomy
    ADD CONSTRAINT isco08_taxonomy_pkey PRIMARY KEY (id);
 M   ALTER TABLE ONLY enums.isco08_taxonomy DROP CONSTRAINT isco08_taxonomy_pkey;
       enums            postgres    false    270            K           2606    1833636 0   orgs_taxonomy_closure orgs_taxonomy_closure_pkey 
   CONSTRAINT        ALTER TABLE ONLY enums.orgs_taxonomy_closure
    ADD CONSTRAINT orgs_taxonomy_closure_pkey PRIMARY KEY (ancestor, descendant);
 Y   ALTER TABLE ONLY enums.orgs_taxonomy_closure DROP CONSTRAINT orgs_taxonomy_closure_pkey;
       enums            postgres    false    274    274            I           2606    1833634     orgs_taxonomy orgs_taxonomy_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY enums.orgs_taxonomy
    ADD CONSTRAINT orgs_taxonomy_pkey PRIMARY KEY (id);
 I   ALTER TABLE ONLY enums.orgs_taxonomy DROP CONSTRAINT orgs_taxonomy_pkey;
       enums            postgres    false    273            M           2606    1833704     rucr_taxonomy rucr_taxonomy_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY enums.rucr_taxonomy
    ADD CONSTRAINT rucr_taxonomy_pkey PRIMARY KEY (id);
 I   ALTER TABLE ONLY enums.rucr_taxonomy DROP CONSTRAINT rucr_taxonomy_pkey;
       enums            postgres    false    276            O           2606    1833706 &   rucr_taxonomy rucr_taxonomy_xml_id_key 
   CONSTRAINT     b   ALTER TABLE ONLY enums.rucr_taxonomy
    ADD CONSTRAINT rucr_taxonomy_xml_id_key UNIQUE (xml_id);
 O   ALTER TABLE ONLY enums.rucr_taxonomy DROP CONSTRAINT rucr_taxonomy_xml_id_key;
       enums            postgres    false    276            Q           2606    1833782    theory_types theory_types_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY enums.theory_types
    ADD CONSTRAINT theory_types_pkey PRIMARY KEY (id);
 G   ALTER TABLE ONLY enums.theory_types DROP CONSTRAINT theory_types_pkey;
       enums            postgres    false    278            S           2606    1833798 *   transfactory_nodes transfactory_nodes_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY enums.transfactory_nodes
    ADD CONSTRAINT transfactory_nodes_pkey PRIMARY KEY (id);
 S   ALTER TABLE ONLY enums.transfactory_nodes DROP CONSTRAINT transfactory_nodes_pkey;
       enums            postgres    false    280            Y           2620    918741    rucr_taxonomy rucr_upup    TRIGGER     x   CREATE TRIGGER rucr_upup BEFORE UPDATE ON enums.rucr_taxonomy FOR EACH ROW EXECUTE FUNCTION public.update_updated_on();
 /   DROP TRIGGER rucr_upup ON enums.rucr_taxonomy;
       enums          postgres    false    276            T           2606    1833920 %   isco08_index isco08_index_isco08_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enums.isco08_index
    ADD CONSTRAINT isco08_index_isco08_fkey FOREIGN KEY (isco08) REFERENCES enums.isco08_taxonomy(id);
 N   ALTER TABLE ONLY enums.isco08_index DROP CONSTRAINT isco08_index_isco08_fkey;
       enums          postgres    false    4165    268    270            U           2606    1833925 =   isco08_taxonomy_closure isco08_taxonomy_closure_ancestor_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enums.isco08_taxonomy_closure
    ADD CONSTRAINT isco08_taxonomy_closure_ancestor_fkey FOREIGN KEY (ancestor) REFERENCES enums.isco08_taxonomy(id);
 f   ALTER TABLE ONLY enums.isco08_taxonomy_closure DROP CONSTRAINT isco08_taxonomy_closure_ancestor_fkey;
       enums          postgres    false    270    4165    271            V           2606    1833930 ?   isco08_taxonomy_closure isco08_taxonomy_closure_descendant_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enums.isco08_taxonomy_closure
    ADD CONSTRAINT isco08_taxonomy_closure_descendant_fkey FOREIGN KEY (descendant) REFERENCES enums.isco08_taxonomy(id);
 h   ALTER TABLE ONLY enums.isco08_taxonomy_closure DROP CONSTRAINT isco08_taxonomy_closure_descendant_fkey;
       enums          postgres    false    4165    270    271            W           2606    1834030 9   orgs_taxonomy_closure orgs_taxonomy_closure_ancestor_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enums.orgs_taxonomy_closure
    ADD CONSTRAINT orgs_taxonomy_closure_ancestor_fkey FOREIGN KEY (ancestor) REFERENCES enums.orgs_taxonomy(id);
 b   ALTER TABLE ONLY enums.orgs_taxonomy_closure DROP CONSTRAINT orgs_taxonomy_closure_ancestor_fkey;
       enums          postgres    false    273    274    4169            X           2606    1834035 ;   orgs_taxonomy_closure orgs_taxonomy_closure_descendant_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY enums.orgs_taxonomy_closure
    ADD CONSTRAINT orgs_taxonomy_closure_descendant_fkey FOREIGN KEY (descendant) REFERENCES enums.orgs_taxonomy(id);
 d   ALTER TABLE ONLY enums.orgs_taxonomy_closure DROP CONSTRAINT orgs_taxonomy_closure_descendant_fkey;
       enums          postgres    false    273    274    4169            �           3256    919261    isco08_index isco08_index_warp    POLICY     L   CREATE POLICY isco08_index_warp ON enums.isco08_index TO warp USING (true);
 5   DROP POLICY isco08_index_warp ON enums.isco08_index;
       enums          postgres    false    268            �           3256    919262    isco08_taxonomy isco8_warp1    POLICY     I   CREATE POLICY isco8_warp1 ON enums.isco08_taxonomy TO warp USING (true);
 2   DROP POLICY isco8_warp1 ON enums.isco08_taxonomy;
       enums          postgres    false    270            �           3256    919263 #   isco08_taxonomy_closure isco8_warp1    POLICY     Q   CREATE POLICY isco8_warp1 ON enums.isco08_taxonomy_closure TO warp USING (true);
 :   DROP POLICY isco8_warp1 ON enums.isco08_taxonomy_closure;
       enums          postgres    false    271            �           3256    919264 +   orgs_taxonomy_closure orgs_tax_closure_warp    POLICY     Y   CREATE POLICY orgs_tax_closure_warp ON enums.orgs_taxonomy_closure TO warp USING (true);
 B   DROP POLICY orgs_tax_closure_warp ON enums.orgs_taxonomy_closure;
       enums          postgres    false    274            �           3256    919265    orgs_taxonomy orgs_tax_warp    POLICY     [   CREATE POLICY orgs_tax_warp ON enums.orgs_taxonomy TO warp USING (true) WITH CHECK (true);
 2   DROP POLICY orgs_tax_warp ON enums.orgs_taxonomy;
       enums          postgres    false    273           