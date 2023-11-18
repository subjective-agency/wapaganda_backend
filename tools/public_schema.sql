PGDMP     
    '    
        
    {            wapadb     15.5 (Ubuntu 15.5-1.pgdg22.04+1)     15.4 (Ubuntu 15.4-2.pgdg22.04+1)    6           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            7           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            8           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            9           1262    16388    wapadb    DATABASE     r   CREATE DATABASE wapadb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE wapadb;
                postgres    false            :           0    0    DATABASE wapadb    ACL     �   GRANT CONNECT ON DATABASE wapadb TO warp;
GRANT CONNECT ON DATABASE wapadb TO transnode2;
GRANT CONNECT ON DATABASE wapadb TO teledummy;
GRANT CONNECT ON DATABASE wapadb TO ata;
GRANT CONNECT ON DATABASE wapadb TO windmill;
                   postgres    false    4665                        2615    917439    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                postgres    false            ;           0    0    SCHEMA public    ACL     {   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO teledummy;
GRANT USAGE ON SCHEMA public TO ata;
                   postgres    false    15            �           1255    917642 3   add_person_with_photo(date, text, text, text, text)    FUNCTION       CREATE FUNCTION public.add_person_with_photo(dob date, fullname_en text, fullname_uk text, fullname_ru text, photo_path text) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare
person_id integer;
photo_id integer;
begin
insert into people (dob, fullname_en, fullname_uk, fullname_ru)
values (dob, fullname_en, fullname_uk, fullname_ru)
returning id into person_id;
insert into photos (path)
values (photo_path)
returning id into photo_id;
insert into people_on_photos (person_id, photo_id)
values (person_id, photo_id);
commit;
end; $$;
 }   DROP FUNCTION public.add_person_with_photo(dob date, fullname_en text, fullname_uk text, fullname_ru text, photo_path text);
       public          postgres    false    15            �           1255    917643 &   add_photo_with_people_v2(text, text[])    FUNCTION     �  CREATE FUNCTION public.add_photo_with_people_v2(path text, fullname_en text[]) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare
photo_id integer;
person_id integer;
fullname text;
begin
insert into photos (path)
values (path)
returning id into photo_id;
foreach fullname in array fullname_en
loop
select id into person_id from people where fullname_en = fullname;
insert into people_on_photos (person_id, photo_id)
values (person_id, photo_id);
end loop;
commit;
end; $$;
 N   DROP FUNCTION public.add_photo_with_people_v2(path text, fullname_en text[]);
       public          postgres    false    15            �           1255    917644 #   channel_stats_last_updated(integer)    FUNCTION     �   CREATE FUNCTION public.channel_stats_last_updated(input_id integer) RETURNS date
    LANGUAGE sql
    AS $$
select max(day_date) from telegram_channels_stats where channel_id = input_id
$$;
 C   DROP FUNCTION public.channel_stats_last_updated(input_id integer);
       public          postgres    false    15            �           1255    917645    copy_registered_duration()    FUNCTION     5  CREATE FUNCTION public.copy_registered_duration() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
tbl text;
tbl_id int;
begin
for i, tbl, tbl_id in
select id, "table", table_id from service.factory_jobs_run_details where registered_duration is null
loop
update service.factory_jobs_run_details set registered_duration = case
when tbl = 'smotrim_episodes' then (select duration from smotrim_episodes where id = tbl_id)
when tbl = 'youtube_vids' then (select duration from youtube_vids where id = tbl_id)
when tbl = 'komso_episodes' then (select duration from komso_episodes where id = tbl_id)
when tbl = 'ntv_episodes' then (select duration from ntv_episodes where id = tbl_id)
when tbl = 'dentv_episodes' then (select duration from dentv_episodes where id = tbl_id)
end
where id = i;
end loop;
end;
$$;
 1   DROP FUNCTION public.copy_registered_duration();
       public          postgres    false    15            �           1255    917646    count_transcribed_lines()    FUNCTION     &  CREATE FUNCTION public.count_transcribed_lines() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
trans_id int;
begin
for i, trans_id in
select id, transcript_id from service.factory_jobs_run_details where transcription_endtime is null
loop
update service.factory_jobs_run_details set transcription_endtime = (SELECT MAX(end_time) FROM data.transcribed_content WHERE transcript_id = trans_id),
transcribed_lines_count = (SELECT COUNT(id) FROM data.transcribed_content WHERE transcript_id = trans_id)
where id = i;
end loop;
end;
$$;
 0   DROP FUNCTION public.count_transcribed_lines();
       public          postgres    false    15            �           1255    917647    count_translated_lines()    FUNCTION     >  CREATE FUNCTION public.count_translated_lines() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
trans_id int;
begin
for i, trans_id in
select id, transcript_id from service.factory_jobs_run_details where translation_endtime is null
loop
update service.factory_jobs_run_details set translation_endtime = (SELECT MAX(end_time) FROM data.transcribed_content_translation_en WHERE transcript_id = trans_id),
translated_lines_count = (SELECT COUNT(id) FROM data.transcribed_content_translation_en WHERE transcript_id = trans_id)
where id = i;
end loop;
end;
$$;
 /   DROP FUNCTION public.count_translated_lines();
       public          postgres    false    15            �           1255    917648 3   createnewuserandprintcredentials(character varying)    FUNCTION     �  CREATE FUNCTION public.createnewuserandprintcredentials(new_username character varying) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
charset TEXT := 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
password_length INT := 10;
password TEXT := '';
BEGIN
FOR i IN 1..password_length LOOP
password := password || substr(charset, floor(1 + random() * 62)::integer, 1);
END LOOP;
EXECUTE 'CREATE USER ' || quote_ident(new_username) || ' WITH PASSWORD ' || quote_literal(password);
RAISE NOTICE 'New user created: Username: %, Password: %', new_username, password;
RETURN 'Username: ' || new_username || ', Password: ' || password;
END;
$$;
 W   DROP FUNCTION public.createnewuserandprintcredentials(new_username character varying);
       public          postgres    false    15                        1255    917649    delete_person(integer)    FUNCTION     q  CREATE FUNCTION public.delete_person(person_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare photo_id integer;
begin
select photo_id from people_on_photos where person_id = person_id into photo_id;
delete from people where id = person_id;
delete from photos where id = photo_id;
delete from people_on_photos where person_id = person_id;
commit;
end; $$;
 7   DROP FUNCTION public.delete_person(person_id integer);
       public          postgres    false    15                       1255    917650    delete_photo(integer)    FUNCTION     �   CREATE FUNCTION public.delete_photo(photo_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
begin
delete from photos where id = photo_id;
delete from people_on_photos where photo_id = photo_id;
commit;
end; $$;
 5   DROP FUNCTION public.delete_photo(photo_id integer);
       public          postgres    false    15                       1255    917651    fix_apostrophe_orgs()    FUNCTION     �   CREATE FUNCTION public.fix_apostrophe_orgs() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
old_symbol TEXT := '''';
new_symbol TEXT := '`';
BEGIN
UPDATE organizations
SET name_uk = REPLACE(name_uk, old_symbol, new_symbol);
COMMIT;
END;
$$;
 ,   DROP FUNCTION public.fix_apostrophe_orgs();
       public          postgres    false    15                       1255    917652    fix_apostrophe_people()    FUNCTION     �   CREATE FUNCTION public.fix_apostrophe_people() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
old_symbol TEXT := '''';
new_symbol TEXT := '`';
BEGIN
UPDATE people
SET fullname_uk = REPLACE(fullname_uk, old_symbol, new_symbol);
COMMIT;
END;
$$;
 .   DROP FUNCTION public.fix_apostrophe_people();
       public          postgres    false    15                       1255    917653    fix_apostrophe_printed()    FUNCTION     �   CREATE FUNCTION public.fix_apostrophe_printed() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
old_symbol TEXT := '''';
new_symbol TEXT := '`';
BEGIN
UPDATE printed
SET title_uk = REPLACE(title_uk, old_symbol, new_symbol);
COMMIT;
END;
$$;
 /   DROP FUNCTION public.fix_apostrophe_printed();
       public          postgres    false    15                       1255    917654    fix_apostrophe_rucr_tax()    FUNCTION       CREATE FUNCTION public.fix_apostrophe_rucr_tax() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
old_symbol TEXT := '''';
new_symbol TEXT := '`';
BEGIN
UPDATE data.rucr_taxonomy
SET content_uk = REPLACE(content_uk, old_symbol, new_symbol);
COMMIT;
END;
$$;
 0   DROP FUNCTION public.fix_apostrophe_rucr_tax();
       public          postgres    false    15                       1255    917655    get_column_comment(text, text)    FUNCTION     
  CREATE FUNCTION public.get_column_comment(table_name text, column_name text, OUT result text) RETURNS text
    LANGUAGE plpgsql
    AS $$
begin
select
*
into
result
from
col_description(get_table_oid(table_name), get_column_subid(table_name, column_name));
end;
$$;
 ]   DROP FUNCTION public.get_column_comment(table_name text, column_name text, OUT result text);
       public          postgres    false    15                       1255    917656    get_column_subid(text, text)    FUNCTION     �   CREATE FUNCTION public.get_column_subid(table_name text, column_name text) RETURNS integer
    LANGUAGE sql
    AS $$
select objsubid from pg_get_object_address('table column', ARRAY[table_name, column_name], '{}')
$$;
 J   DROP FUNCTION public.get_column_subid(table_name text, column_name text);
       public          postgres    false    15                       1255    917657    get_default_photo(text, text)    FUNCTION     �  CREATE FUNCTION public.get_default_photo(pic_type text, sex text) RETURNS text
    LANGUAGE sql
    AS $$
select
case when pic_type = 'large' and sex = 'm'
then (select url from photos where id = 1)
when pic_type = 'thumb' and sex = 'm'
then (select url from photos where id = 2)
when pic_type = 'large' and sex = 'f'
then (select url from photos where id = 3)
when pic_type = 'thumb' and sex = 'f'
then (select url from photos where id = 4)
end;
$$;
 A   DROP FUNCTION public.get_default_photo(pic_type text, sex text);
       public          postgres    false    15            	           1255    917658    get_komso_have_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_komso_have_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from komso_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 ;   DROP FUNCTION public.get_komso_have_count(seg_id integer);
       public          postgres    false    15            
           1255    917659     get_komso_have_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_komso_have_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from komso_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 >   DROP FUNCTION public.get_komso_have_duration(seg_id integer);
       public          postgres    false    15                       1255    917660     get_komso_overall_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_komso_overall_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from komso_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 >   DROP FUNCTION public.get_komso_overall_count(seg_id integer);
       public          postgres    false    15                       1255    917661 #   get_komso_overall_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_komso_overall_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from komso_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 A   DROP FUNCTION public.get_komso_overall_duration(seg_id integer);
       public          postgres    false    15            �           1255    917662     get_komso_segment_stats(integer)    FUNCTION     A  CREATE FUNCTION public.get_komso_segment_stats(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from komso_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 >   DROP FUNCTION public.get_komso_segment_stats(seg_id integer);
       public          postgres    false    15            �           1255    917663 "   get_komso_segment_stats_h(integer)    FUNCTION     T  CREATE FUNCTION public.get_komso_segment_stats_h(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from komso_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_komso_segment_stats_h(seg_id integer);
       public          postgres    false    15                       1255    917664 $   get_komso_unavailable_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_komso_unavailable_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from komso_episodes
where segment_id = seg_id and need is not false and have is not true and url_is_alive is false;
$$;
 B   DROP FUNCTION public.get_komso_unavailable_count(seg_id integer);
       public          postgres    false    15                       1255    917665 '   get_komso_unavailable_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_komso_unavailable_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from komso_episodes
where segment_id = seg_id and need is not false and have is not true and url_is_alive is false;
$$;
 E   DROP FUNCTION public.get_komso_unavailable_duration(seg_id integer);
       public          postgres    false    15                       1255    917666    get_ntv_have_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_ntv_have_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from ntv_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 9   DROP FUNCTION public.get_ntv_have_count(seg_id integer);
       public          postgres    false    15                       1255    917667    get_ntv_have_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_ntv_have_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from ntv_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 <   DROP FUNCTION public.get_ntv_have_duration(seg_id integer);
       public          postgres    false    15                       1255    917668    get_ntv_overall_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_ntv_overall_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from ntv_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 <   DROP FUNCTION public.get_ntv_overall_count(seg_id integer);
       public          postgres    false    15                       1255    917669 !   get_ntv_overall_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_ntv_overall_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from ntv_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 ?   DROP FUNCTION public.get_ntv_overall_duration(seg_id integer);
       public          postgres    false    15                       1255    917670    get_ntv_segment_stats(integer)    FUNCTION     =  CREATE FUNCTION public.get_ntv_segment_stats(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from ntv_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 <   DROP FUNCTION public.get_ntv_segment_stats(seg_id integer);
       public          postgres    false    15                       1255    917671     get_ntv_segment_stats_h(integer)    FUNCTION     P  CREATE FUNCTION public.get_ntv_segment_stats_h(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from ntv_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 >   DROP FUNCTION public.get_ntv_segment_stats_h(seg_id integer);
       public          postgres    false    15                       1255    917672    get_org_people(bigint)    FUNCTION     c  CREATE FUNCTION public.get_org_people(oid bigint) RETURNS jsonb[]
    LANGUAGE sql STRICT
    AS $$
SELECT array_agg(jsonb_build_object('id', p.id, 'name', p.fullname_en, 'role', iindex.name_en))
FROM people p
LEFT JOIN people_in_orgs pio ON p.id = pio.person_id
LEFT JOIN enums.isco08_index iindex ON pio.role_ref = iindex.id
WHERE oid = pio.org_id;
$$;
 1   DROP FUNCTION public.get_org_people(oid bigint);
       public          postgres    false    15                       1255    917673 "   get_organization_ancestors(bigint)    FUNCTION     |  CREATE FUNCTION public.get_organization_ancestors(org_id bigint) RETURNS jsonb[]
    LANGUAGE sql
    AS $$
WITH RECURSIVE org_hierarchy AS (
SELECT id, name_en, short_name, org_type, parent_org_id, 1 AS level
FROM organizations
WHERE id = org_id
UNION ALL
SELECT o.id, o.name_en, o.short_name, o.org_type, o.parent_org_id, h.level + 1
FROM organizations o
INNER JOIN org_hierarchy h ON o.id = h.parent_org_id
WHERE o.id != org_id
)
SELECT array_agg(jsonb_build_object(
'id', o.id,
'name_en', o.name_en,
'short_name', o.short_name,
'org_type', o.org_type
) ORDER BY h.level)
FROM org_hierarchy h
JOIN organizations o ON h.id = o.id
$$;
 @   DROP FUNCTION public.get_organization_ancestors(org_id bigint);
       public          postgres    false    15                       1255    917674 #   get_organization_ancestors1(bigint)    FUNCTION     }  CREATE FUNCTION public.get_organization_ancestors1(org_id bigint) RETURNS jsonb[]
    LANGUAGE sql
    AS $$
WITH RECURSIVE org_hierarchy AS (
SELECT id, name_en, short_name, org_type, parent_org_id, 1 AS level
FROM organizations
WHERE id = org_id
UNION ALL
SELECT o.id, o.name_en, o.short_name, o.org_type, o.parent_org_id, h.level + 1
FROM organizations o
INNER JOIN org_hierarchy h ON o.id = h.parent_org_id
WHERE o.id != org_id
)
SELECT array_agg(jsonb_build_object(
'id', o.id,
'name_en', o.name_en,
'short_name', o.short_name,
'org_type', o.org_type
) ORDER BY h.level)
FROM org_hierarchy h
JOIN organizations o ON h.id = o.id
$$;
 A   DROP FUNCTION public.get_organization_ancestors1(org_id bigint);
       public          postgres    false    15                       1255    917675    get_orgs_data(integer[])    FUNCTION     �  CREATE FUNCTION public.get_orgs_data(ids integer[]) RETURNS jsonb[]
    LANGUAGE plpgsql
    AS $$
DECLARE
result JSONB[];
record_data RECORD;
BEGIN
FOR record_data IN
SELECT o.id id, o.name_en name_en, o.name_ru name_ru, o.name_uk name_uk,
ot.org_type org_type,
op.name_ru parent_org_name, op.id parent_org_id,
o.source_url url, o.short_name short_name, o.state_affiliated state_aff, o.org_form org_form
FROM organizations o
LEFT JOIN organization_type ot on ot.id = o.org_type_id
LEFT JOIN organizations op on o.parent_org_id = op.id
WHERE o.id = ANY(ids)
LOOP
result := result || jsonb_build_object(
'id', record_data.id,
'name_ru', record_data.name_ru,
'name_en', record_data.name_en,
'name_uk', record_data.name_uk,
'org_type', record_data.org_type,
'parent_org_name', record_data.parent_org_name,
'parent_org_id', record_data.parent_org_id,
'url', record_data.url,
'short_name', record_data.short_name,
'state_affiliated', record_data.state_aff,
'org_form', record_data.org_form
);
END LOOP;
RETURN result;
END;
$$;
 3   DROP FUNCTION public.get_orgs_data(ids integer[]);
       public          postgres    false    15                       1255    917676    get_patient_orgs(bigint)    FUNCTION     �   CREATE FUNCTION public.get_patient_orgs(oid bigint) RETURNS integer[]
    LANGUAGE sql STRICT
    AS $$
select array_agg(o.id)
from organizations o
left join people_in_orgs pio on o.id = pio.org_id
where oid = pio.person_id
$$;
 3   DROP FUNCTION public.get_patient_orgs(oid bigint);
       public          postgres    false    15                       1255    917677    get_patient_orgs_idx(bigint)    FUNCTION     �   CREATE FUNCTION public.get_patient_orgs_idx(oid bigint) RETURNS integer[]
    LANGUAGE sql STRICT
    AS $$
select array_agg(o.id)
from organizations o
left join people_in_orgs pio on o.id = pio.org_id
where oid = pio.person_id
$$;
 7   DROP FUNCTION public.get_patient_orgs_idx(oid bigint);
       public          postgres    false    15                       1255    917678 !   get_patient_tchannels_idx(bigint)    FUNCTION     �   CREATE FUNCTION public.get_patient_tchannels_idx(oid bigint) RETURNS integer[]
    LANGUAGE sql STRICT
    AS $$
select array_agg(t.id)
from telegram_channels t
left join telegram_authors ta on t.id = ta.channel_id
where oid = ta.person_id
$$;
 <   DROP FUNCTION public.get_patient_tchannels_idx(oid bigint);
       public          postgres    false    15                       1255    917679 !   get_patient_ychannels_idx(bigint)    FUNCTION     �   CREATE FUNCTION public.get_patient_ychannels_idx(oid bigint) RETURNS integer[]
    LANGUAGE sql STRICT
    AS $$
select array_agg(yc.id)
from youtube_channels yc
left join youtube_authors ya on yc.id = ya.channel_id
where oid = ya.person_id
$$;
 <   DROP FUNCTION public.get_patient_ychannels_idx(oid bigint);
       public          postgres    false    15                       1255    917680    get_person_bundles(integer)    FUNCTION     U  CREATE FUNCTION public.get_person_bundles(pid integer) RETURNS jsonb[]
    LANGUAGE sql STRICT
    AS $$
SELECT array_agg(
jsonb_build_object(
'id', pb.id,
'bundle_name', pb.bundle_name,
'bundle_type', pb.bundle_type
)
)
FROM people_bundles pb
LEFT JOIN people_in_bundles p_in_b ON pb.id = p_in_b.bundle_id
WHERE p_in_b.person_id = pid;
$$;
 6   DROP FUNCTION public.get_person_bundles(pid integer);
       public          postgres    false    15                       1255    917681 "   get_person_external_links(integer)    FUNCTION     �   CREATE FUNCTION public.get_person_external_links(pid integer) RETURNS text[]
    LANGUAGE sql STRICT
    AS $$
select string_to_array(replace(replace(url, '{', ''), '}', ''), ',')
from people_3rdprt_details_raw
where person_id = pid
$$;
 =   DROP FUNCTION public.get_person_external_links(pid integer);
       public          postgres    false    15                       1255    917682    get_person_photo(integer, text)    FUNCTION       CREATE FUNCTION public.get_person_photo(pid integer, pic_type text) RETURNS text
    LANGUAGE sql STRICT
    AS $$
select ph.url
from photos ph
left join people_on_photos pop on pop.photo_id = ph.id
left join people p on pop.person_id = p.id
where p.id = pid and ph.type = pic_type
$$;
 C   DROP FUNCTION public.get_person_photo(pid integer, pic_type text);
       public          postgres    false    15                        1255    917683    get_smotrim_have_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_smotrim_have_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from smotrim_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 =   DROP FUNCTION public.get_smotrim_have_count(seg_id integer);
       public          postgres    false    15            !           1255    917684 "   get_smotrim_have_duration(integer)    FUNCTION        CREATE FUNCTION public.get_smotrim_have_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from smotrim_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_smotrim_have_duration(seg_id integer);
       public          postgres    false    15            "           1255    917685 "   get_smotrim_overall_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_smotrim_overall_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from smotrim_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_smotrim_overall_count(seg_id integer);
       public          postgres    false    15            #           1255    917686 %   get_smotrim_overall_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_smotrim_overall_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from smotrim_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 C   DROP FUNCTION public.get_smotrim_overall_duration(seg_id integer);
       public          postgres    false    15            $           1255    917687 "   get_smotrim_segment_stats(integer)    FUNCTION     E  CREATE FUNCTION public.get_smotrim_segment_stats(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from smotrim_episodes
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_smotrim_segment_stats(seg_id integer);
       public          postgres    false    15            %           1255    917688 $   get_smotrim_segment_stats_h(integer)    FUNCTION     X  CREATE FUNCTION public.get_smotrim_segment_stats_h(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from smotrim_episodes
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 B   DROP FUNCTION public.get_smotrim_segment_stats_h(seg_id integer);
       public          postgres    false    15            &           1255    917689 &   get_smotrim_unavailable_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_smotrim_unavailable_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from smotrim_episodes
where segment_id = seg_id and need is not false and have is not true and url_is_alive is false;
$$;
 D   DROP FUNCTION public.get_smotrim_unavailable_count(seg_id integer);
       public          postgres    false    15            '           1255    917690 )   get_smotrim_unavailable_duration(integer)    FUNCTION       CREATE FUNCTION public.get_smotrim_unavailable_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from smotrim_episodes
where segment_id = seg_id and need is not false and have is not true and url_is_alive is false;
$$;
 G   DROP FUNCTION public.get_smotrim_unavailable_duration(seg_id integer);
       public          postgres    false    15            (           1255    917691    get_table_oid(text)    FUNCTION     �   CREATE FUNCTION public.get_table_oid(table_name text) RETURNS integer
    LANGUAGE sql
    AS $$
select objid from pg_get_object_address('table', ARRAY[table_name], '{}')
$$;
 5   DROP FUNCTION public.get_table_oid(table_name text);
       public          postgres    false    15            )           1255    917692 #   get_tchannel_history_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_tchannel_history_count(c_id integer) RETURNS integer
    LANGUAGE sql STRICT
    AS $$
select count(origin_id)
from data.telegram_messages
where channel_id = c_id
$$;
 ?   DROP FUNCTION public.get_tchannel_history_count(c_id integer);
       public          postgres    false    15            *           1255    917693    get_tchannel_max_date(integer)    FUNCTION     �   CREATE FUNCTION public.get_tchannel_max_date(c_id integer) RETURNS date
    LANGUAGE sql STRICT
    AS $$
select max(date_publish)
from data.telegram_messages
where channel_id = c_id
$$;
 :   DROP FUNCTION public.get_tchannel_max_date(c_id integer);
       public          postgres    false    15            +           1255    917694 #   get_tchannel_max_origin_id(integer)    FUNCTION     �   CREATE FUNCTION public.get_tchannel_max_origin_id(c_id integer) RETURNS integer
    LANGUAGE sql STRICT
    AS $$
select max(origin_id)
from data.telegram_messages
where channel_id = c_id
$$;
 ?   DROP FUNCTION public.get_tchannel_max_origin_id(c_id integer);
       public          postgres    false    15            ,           1255    917695    get_tchannels_data(integer[])    FUNCTION     �  CREATE FUNCTION public.get_tchannels_data(ids integer[]) RETURNS jsonb[]
    LANGUAGE plpgsql
    AS $$
DECLARE
result JSONB[];
record_data RECORD;
BEGIN
FOR record_data IN
SELECT tch.id, tch.handle, tch.title, tch.telemetr_id, tch.population, tch.date_created, tch.status, tch.description, tch.history_count
FROM telegram_channels tch
WHERE tch.id = ANY(ids)
LOOP
result := result || jsonb_build_object(
'id', record_data.id,
'handle', record_data.handle,
'title', record_data.title,
'telemetr_id', record_data.telemetr_id,
'population', record_data.population,
'date_created', record_data.date_created,
'status', record_data.status,
'description', record_data.description,
'history_count', record_data.history_count
);
END LOOP;
RETURN result;
END;
$$;
 8   DROP FUNCTION public.get_tchannels_data(ids integer[]);
       public          postgres    false    15            -           1255    917696    get_transcribed_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_transcribed_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from data.transcripts
where segment_id = seg_id;
$$;
 <   DROP FUNCTION public.get_transcribed_count(seg_id integer);
       public          postgres    false    15            .           1255    917697 !   get_transcribed_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_transcribed_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from data.transcripts
where segment_id = seg_id;
$$;
 ?   DROP FUNCTION public.get_transcribed_duration(seg_id integer);
       public          postgres    false    15            /           1255    917698 $   get_transcribed_lines_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_transcribed_lines_count(idx integer) RETURNS integer
    LANGUAGE sql
    AS $$
SELECT count(*)
FROM data.transcribed_content
WHERE transcript_id = idx
$$;
 ?   DROP FUNCTION public.get_transcribed_lines_count(idx integer);
       public          postgres    false    15            0           1255    917699    get_transcribed_stats(integer)    FUNCTION       CREATE FUNCTION public.get_transcribed_stats(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from data.transcripts
where segment_id = seg_id;
$$;
 <   DROP FUNCTION public.get_transcribed_stats(seg_id integer);
       public          postgres    false    15            1           1255    917700    get_ychannels_data(integer[])    FUNCTION     �  CREATE FUNCTION public.get_ychannels_data(ids integer[]) RETURNS jsonb[]
    LANGUAGE plpgsql
    AS $$
DECLARE
result JSONB[];
record_data RECORD;
BEGIN
FOR record_data IN
SELECT ych.id, ych.youtube_id, ych.title, ych.subs_count, ych.date_created, ych.vids_count, ych.views_count, ych.status, ych.description
FROM youtube_channels ych
WHERE ych.id = ANY(ids)
LOOP
result := result || jsonb_build_object(
'id', record_data.id,
'handle', record_data.youtube_id,
'title', record_data.title,
'population', record_data.subs_count,
'date_created', record_data.date_created,
'status', record_data.status,
'description', record_data.description,
'history_count', record_data.vids_count,
'views', record_data.views_count
);
END LOOP;
RETURN result;
END;
$$;
 8   DROP FUNCTION public.get_ychannels_data(ids integer[]);
       public          postgres    false    15            2           1255    917701    get_youtube_have_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_youtube_have_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from youtube_vids
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 =   DROP FUNCTION public.get_youtube_have_count(seg_id integer);
       public          postgres    false    15            3           1255    917702 "   get_youtube_have_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_youtube_have_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from youtube_vids
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_youtube_have_duration(seg_id integer);
       public          postgres    false    15            4           1255    917703 "   get_youtube_overall_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_youtube_overall_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from youtube_vids
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_youtube_overall_count(seg_id integer);
       public          postgres    false    15            5           1255    917704 %   get_youtube_overall_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_youtube_overall_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from youtube_vids
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 C   DROP FUNCTION public.get_youtube_overall_duration(seg_id integer);
       public          postgres    false    15            6           1255    917705 "   get_youtube_segment_stats(integer)    FUNCTION     A  CREATE FUNCTION public.get_youtube_segment_stats(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from youtube_vids
where segment_id = seg_id and need is not false and timestamp_aired > '2021-11-01';
$$;
 @   DROP FUNCTION public.get_youtube_segment_stats(seg_id integer);
       public          postgres    false    15            7           1255    917706 $   get_youtube_segment_stats_h(integer)    FUNCTION     T  CREATE FUNCTION public.get_youtube_segment_stats_h(seg_id integer) RETURNS TABLE(total_count integer, total_duration integer)
    LANGUAGE sql
    AS $$
select count(*) as total_count, sum(duration) as total_duration
from youtube_vids
where segment_id = seg_id and need is not false and have is true and timestamp_aired > '2021-11-01';
$$;
 B   DROP FUNCTION public.get_youtube_segment_stats_h(seg_id integer);
       public          postgres    false    15            8           1255    917707 &   get_youtube_unavailable_count(integer)    FUNCTION     �   CREATE FUNCTION public.get_youtube_unavailable_count(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select count(id)
from youtube_vids
where segment_id = seg_id and need is not false and have is not true and url_is_alive is false;
$$;
 D   DROP FUNCTION public.get_youtube_unavailable_count(seg_id integer);
       public          postgres    false    15            9           1255    917708 )   get_youtube_unavailable_duration(integer)    FUNCTION     �   CREATE FUNCTION public.get_youtube_unavailable_duration(seg_id integer) RETURNS integer
    LANGUAGE sql
    AS $$
select sum(duration)
from youtube_vids
where segment_id = seg_id and need is not false and have is not true and url_is_alive is false;
$$;
 G   DROP FUNCTION public.get_youtube_unavailable_duration(seg_id integer);
       public          postgres    false    15            :           1255    917709    grant_privileges(text)    FUNCTION     p  CREATE FUNCTION public.grant_privileges(username text) RETURNS void
    LANGUAGE sql
    AS $$
grant connect on database postgres to username;
grant pg_read_all_data to username;
grant pg_write_all_data to username;
grant usage on schema public to username;
grant usage on schema service to username;
grant usage on schema data to username;
grant usage on schema future to username;
grant all privileges on all tables in schema public to username;
grant all privileges on all tables in schema service to username;
grant all privileges on all tables in schema data to username;
grant all privileges on all tables in schema future to username;
grant all privileges on all sequences in schema public to username;
grant all privileges on all sequences in schema service to username;
grant all privileges on all sequences in schema data to username;
grant all privileges on all sequences in schema future to username;
grant all privileges on all functions in schema public to username;
grant all privileges on all functions in schema service to username;
grant all privileges on all functions in schema data to username;
grant all privileges on all functions in schema future to username;
alter default privileges in schema public grant all on tables to username;
alter default privileges in schema service grant all on tables to username;
alter default privileges in schema data grant all on tables to username;
alter default privileges in schema future grant all on tables to username;
alter default privileges in schema public grant all on functions to username;
alter default privileges in schema service grant all on functions to username;
alter default privileges in schema data grant all on functions to username;
alter default privileges in schema future grant all on functions to username;
alter default privileges in schema public grant all on sequences to username;
alter default privileges in schema service grant all on sequences to username;
alter default privileges in schema data grant all on sequences to username;
alter default privileges in schema future grant all on sequences to username;
alter user username set statement_timeout = '10s';
$$;
 6   DROP FUNCTION public.grant_privileges(username text);
       public          postgres    false    15            ;           1255    917710    insert_new_prabyss()    FUNCTION     �   CREATE FUNCTION public.insert_new_prabyss() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
INSERT INTO service.factory_jobs_run_details (prabyss_id) VALUES (NEW.id);
RETURN NEW;
END;
$$;
 +   DROP FUNCTION public.insert_new_prabyss();
       public          postgres    false    15            <           1255    917711    latest_update_date(integer)    FUNCTION     �   CREATE FUNCTION public.latest_update_date(input_id integer) RETURNS date
    LANGUAGE sql
    AS $$
select max(day_date) from telegram_channels_stats where id = input_id
$$;
 ;   DROP FUNCTION public.latest_update_date(input_id integer);
       public          postgres    false    15            =           1255    917712    resolve_no_duration()    FUNCTION       CREATE FUNCTION public.resolve_no_duration() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
dur int;
smo_id int;
yt_id int;
kms_id int;
n_id int;
d_id int;
begin
for i, smo_id, yt_id, kms_id, n_id, d_id in
select id, smotrim_id, youtube_id, komso_id, ntv_id, dentv_id from data.transcripts where duration is null
loop
select end_time from data.transcribed_content where transcript_id = i order by int_sequence desc limit 1 into dur;
update data.transcripts set duration = dur::int where id = i;
update smotrim_episodes set duration = case when smo_id is not null then dur::int end where id = smo_id;
update youtube_vids set duration = case when yt_id is not null then dur::int end where id = yt_id;
update komso_episodes set duration = case when kms_id is not null then dur::int end where id = kms_id;
update ntv_episodes set duration = case when n_id is not null then dur::int end where id = n_id;
update dentv_episodes set duration = case when d_id is not null then dur::int end where id = d_id;
end loop;
end;
$$;
 ,   DROP FUNCTION public.resolve_no_duration();
       public          postgres    false    15            >           1255    917713    resolve_no_duration_smotrim()    FUNCTION     �  CREATE FUNCTION public.resolve_no_duration_smotrim() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
res int;
begin
for i in
select id from smotrim_episodes where duration is null
loop
select id from data.transcripts where smotrim_id = i into res;
update smotrim_episodes set duration = case
when res is not null
then (select end_time from data.transcribed_content where transcript_id = res order by int_sequence desc limit 1)::int end
where id = i;
end loop;
end;
$$;
 4   DROP FUNCTION public.resolve_no_duration_smotrim();
       public          postgres    false    15            ?           1255    917714 !   resolve_no_duration_transcripts()    FUNCTION     ~  CREATE FUNCTION public.resolve_no_duration_transcripts() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
begin
for i in
select id from data.transcripts where duration is null
loop
update data.transcripts set duration = (select end_time from data.transcribed_content where transcript_id = i order by int_sequence desc limit 1)::int where id = i;
end loop;
end;
$$;
 8   DROP FUNCTION public.resolve_no_duration_transcripts();
       public          postgres    false    15            @           1255    917715    resolve_no_segment()    FUNCTION     O  CREATE FUNCTION public.resolve_no_segment() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
seg_id int;
smo_id int;
yt_id int;
kms_id int;
n_id int;
d_id int;
begin
for i, smo_id, yt_id, kms_id, n_id, d_id in
select id, smotrim_id, youtube_id, komso_id, ntv_id, dentv_id from data.transcripts where segment_id is null
loop
update data.transcripts set segment_id = case
when smo_id is not null then (select segment_id from smotrim_episodes where id = smo_id)
when yt_id is not null then (select segment_id from youtube_vids where id = yt_id)
when kms_id is not null then (select segment_id from komso_episodes where id = kms_id)
when n_id is not null then (select segment_id from ntv_episodes where id = n_id)
when d_id is not null then (select segment_id from dentv_episodes where id = d_id)
end
where id = i;
end loop;
end;
$$;
 +   DROP FUNCTION public.resolve_no_segment();
       public          postgres    false    15            A           1255    917716    search_in_isco8(text)    FUNCTION     	  CREATE FUNCTION public.search_in_isco8(search_term text) RETURNS TABLE(term_id integer, term text, code text, definition text)
    LANGUAGE sql
    AS $$
select id term_id, term, isco_code code, definition
from enums.isco08_taxonomy
where term &@~ search_term;
$$;
 8   DROP FUNCTION public.search_in_isco8(search_term text);
       public          postgres    false    15            B           1255    917717    search_in_isco8_index(text)    FUNCTION     �  CREATE FUNCTION public.search_in_isco8_index(search_term text) RETURNS TABLE(term_id integer, index_id integer, name_en text, code text, definition text, category text)
    LANGUAGE sql
    AS $$
select ii.isco08 term_id, ii.id index_id, ii.name_en, it.isco_code code, it.definition, it.term category
from enums.isco08_index ii
left join enums.isco08_taxonomy it on ii.isco08 = it.id
where ii.name_en &@~ search_term or it.term &@~ search_term;
$$;
 >   DROP FUNCTION public.search_in_isco8_index(search_term text);
       public          postgres    false    15            C           1255    917718    search_in_komso_episodes(text)    FUNCTION     �  CREATE FUNCTION public.search_in_komso_episodes(search_term text) RETURNS TABLE(id integer, title text, segment_id integer, smotrim_id text, duration integer, description text, timestamp_aired timestamp without time zone)
    LANGUAGE sql
    AS $$
select id, title, segment_id, komso_id, duration, description, timestamp_aired
from komso_episodes
where title &@ search_term or description &@ search_term;
$$;
 A   DROP FUNCTION public.search_in_komso_episodes(search_term text);
       public          postgres    false    15            D           1255    917719    search_in_ntv_episodes(text)    FUNCTION     �  CREATE FUNCTION public.search_in_ntv_episodes(search_term text) RETURNS TABLE(id integer, title text, segment_id integer, ntv_id integer, duration integer, description text, timeline jsonb, timestamp_aired timestamp without time zone)
    LANGUAGE sql
    AS $$
select id, title, segment_id, ntv_id, duration, description, timeline, timestamp_aired
from ntv_episodes
where title &@~ search_term or description &@~ search_term;
$$;
 ?   DROP FUNCTION public.search_in_ntv_episodes(search_term text);
       public          postgres    false    15            E           1255    917720    search_in_orgs(text)    FUNCTION     �  CREATE FUNCTION public.search_in_orgs(search_term text) RETURNS TABLE(id integer, name_en text, name_ru text, source_url text, org_type_id integer, short_name jsonb, org_form jsonb)
    LANGUAGE sql
    AS $$
select id, name_en, name_ru, source_url, org_type_id, short_name, org_form
from organizations
where name_en &@~ search_term or name_ru &@~ search_term or short_name &@~ search_term;
$$;
 7   DROP FUNCTION public.search_in_orgs(search_term text);
       public          postgres    false    15            F           1255    917721    search_in_orgs_taxonomy(text)    FUNCTION       CREATE FUNCTION public.search_in_orgs_taxonomy(search_term text) RETURNS TABLE(cat_id integer, category text, code text, definition text)
    LANGUAGE sql
    AS $$
select id cat_id, term category, code, definition
from enums.orgs_taxonomy
where term &@~ search_term;
$$;
 @   DROP FUNCTION public.search_in_orgs_taxonomy(search_term text);
       public          postgres    false    15                       1255    2582510    search_in_people(text)    FUNCTION       CREATE FUNCTION public.search_in_people(search_query text) RETURNS TABLE(id integer, fullname_uk text, fullname_ru text, fullname_en text, lastname_en text, lastname_ru text, social text[], dob timestamp without time zone, contact jsonb, address text[], associates jsonb[], additional jsonb, aliases jsonb[], info jsonb, dod timestamp without time zone, cod text, known_for jsonb, wiki_ref jsonb, photo text, external_links text[], bundles jsonb[], thumb text, added_on timestamp without time zone, orgs jsonb[], sex text, telegram_channels jsonb[], youtube_channels jsonb[])
    LANGUAGE sql
    AS $$
	select pe.id, pe.fullname_uk, pe.fullname_ru, pe.fullname_en, pe.lastname_en, pe.lastname_ru, pe.social, pe.dob,
	pe.contact, pe.address, pe.associates, pe.additional, pe.aliases, pe.info, pe.dod, pe.cod, pe.known_for, pe.wiki_ref,
	pe.photo, pe.external_links, pe.bundles, pe.thumb, pe.added_on, pe.orgs, pe.sex, pe.telegram_channels, pe.youtube_channels
	from public.people_extended pe
	join public.people p on pe.id = p.id
    where p.fullname_ru &@~ search_query or p.fullname_en &@~ search_query or p.fullname_uk &@~ search_query;
$$;
 :   DROP FUNCTION public.search_in_people(search_query text);
       public          postgres    false    15            G           1255    917722    search_in_people_skim(text)    FUNCTION     [  CREATE FUNCTION public.search_in_people_skim(search_query text) RETURNS TABLE(id integer, fullname_ru text, fullname_en text, dob date, known_for text)
    LANGUAGE sql
    AS $$
select id, fullname_ru, fullname_en, dob, known_for
from people
where fullname_ru &@~ search_query or fullname_en &@~ search_query or fullname_uk &@~ search_query;
$$;
 ?   DROP FUNCTION public.search_in_people_skim(search_query text);
       public          postgres    false    15            H           1255    917723    search_in_printed(text)    FUNCTION       CREATE FUNCTION public.search_in_printed(search_term text) RETURNS TABLE(printed_id integer, int_sequence integer, raw_content text)
    LANGUAGE sql
    AS $$
select printed_id, int_sequence, raw_content
from data.printed_content
where raw_content &@~ search_term;
$$;
 :   DROP FUNCTION public.search_in_printed(search_term text);
       public          postgres    false    15            I           1255    917724     search_in_smotrim_episodes(text)    FUNCTION     �  CREATE FUNCTION public.search_in_smotrim_episodes(search_term text) RETURNS TABLE(id integer, title text, segment_id integer, smotrim_id text, duration integer, description text, timestamp_aired timestamp without time zone)
    LANGUAGE sql
    AS $$
select id, title, segment_id, smotrim_id, duration, description, timestamp_aired
from smotrim_episodes
where title &@~ search_term or description &@~ search_term;
$$;
 C   DROP FUNCTION public.search_in_smotrim_episodes(search_term text);
       public          postgres    false    15            J           1255    917725    search_in_transcribed(text)    FUNCTION       CREATE FUNCTION public.search_in_transcribed(search_term text) RETURNS TABLE(transcript_id integer, int_sequence integer, content text)
    LANGUAGE sql
    AS $$
select transcript_id, int_sequence, content
from data.transcribed_content
where content &@~ search_term;
$$;
 >   DROP FUNCTION public.search_in_transcribed(search_term text);
       public          postgres    false    15            K           1255    917726    search_in_youtube_vids(text)    FUNCTION     �  CREATE FUNCTION public.search_in_youtube_vids(search_term text) RETURNS TABLE(id integer, title text, segment_id integer, youtube_id text, duration integer, description text, youtube_channel_id integer, timestamp_aired timestamp without time zone)
    LANGUAGE sql
    AS $$
select id, title, segment_id, youtube_id, duration, description, youtube_channel_id, timestamp_aired
from youtube_vids
where title &@~ search_term or description &@~ search_term;
$$;
 ?   DROP FUNCTION public.search_in_youtube_vids(search_term text);
       public          postgres    false    15            L           1255    917727    updat_date_published()    FUNCTION     �   CREATE FUNCTION public.updat_date_published() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
NEW.first_date_datetime = (SELECT (original_content_metadata->0->>'date_published')::timestamp FROM theory WHERE id = NEW.id);
RETURN NEW;
END;
$$;
 -   DROP FUNCTION public.updat_date_published();
       public          postgres    false    15            M           1255    917728    update_date_published()    FUNCTION     ]  CREATE FUNCTION public.update_date_published() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF NEW.original_content_metadata IS NOT NULL AND array_length(NEW.original_content_metadata, 1) > 0 THEN
NEW.publish_date = (NEW.original_content_metadata[1]->>'date_published')::timestamp;
ELSE
NEW.publish_date = NULL;
END IF;
RETURN NEW;
END;
$$;
 .   DROP FUNCTION public.update_date_published();
       public          postgres    false    15            
           1255    917729    update_dow()    FUNCTION     b  CREATE FUNCTION public.update_dow() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
    i date := (select max(day_date)::date from public.days_of_war);
begin
	while i < now()::date loop
    insert into public.days_of_war (day_date) values((i + '1 day'::interval)::date);
    i := (i + '1 day'::interval)::date;
    end loop;
end;
$$;
 #   DROP FUNCTION public.update_dow();
       public          postgres    false    15            N           1255    917730 $   update_komso_msegments_latest_date()    FUNCTION     k  CREATE FUNCTION public.update_komso_msegments_latest_date() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
begin
for i in
select id from media_segments where relevant is true and komso_id is not null
loop
update media_segments set latest_episode_date = (select max(timestamp_aired) from komso_episodes where segment_id = i);
end loop;
end;
$$;
 ;   DROP FUNCTION public.update_komso_msegments_latest_date();
       public          postgres    false    15            O           1255    917731    update_komso_segments_stats()    FUNCTION     c  CREATE FUNCTION public.update_komso_segments_stats() RETURNS void
    LANGUAGE plpgsql
    AS $$
begin
insert into service.media_segments_stats (segment_id, day_date, total, total_time, have, have_time, transcribed, transcribed_time)
select id, now()::date, ks.total_count, ks.total_duration, kh.total_count, kh.total_duration, kt.total_count, kt.total_duration
from media_segments
inner join lateral get_komso_segment_stats(id) ks on true
inner join lateral get_komso_segment_stats_h(id) kh on true
inner join lateral get_transcribed_stats(id) kt on true
where relevant is true and cluster = 'komso';
end;
$$;
 4   DROP FUNCTION public.update_komso_segments_stats();
       public          postgres    false    15            P           1255    917732 "   update_ntv_msegments_latest_date()    FUNCTION     e  CREATE FUNCTION public.update_ntv_msegments_latest_date() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
begin
for i in
select id from media_segments where relevant is true and ntv_id is not null
loop
update media_segments set latest_episode_date = (select max(timestamp_aired) from ntv_episodes where segment_id = i);
end loop;
end;
$$;
 9   DROP FUNCTION public.update_ntv_msegments_latest_date();
       public          postgres    false    15            Q           1255    917733    update_ntv_segments_stats()    FUNCTION     [  CREATE FUNCTION public.update_ntv_segments_stats() RETURNS void
    LANGUAGE plpgsql
    AS $$
begin
insert into service.media_segments_stats (segment_id, day_date, total, total_time, have, have_time, transcribed, transcribed_time)
select id, now()::date, ys.total_count, ys.total_duration, yh.total_count, yh.total_duration, yt.total_count, yt.total_duration
from media_segments
inner join lateral get_ntv_segment_stats(id) ys on true
inner join lateral get_ntv_segment_stats_h(id) yh on true
inner join lateral get_transcribed_stats(id) yt on true
where relevant is true and cluster = 'ntv';
end;
$$;
 2   DROP FUNCTION public.update_ntv_segments_stats();
       public          postgres    false    15            R           1255    917734 &   update_smotrim_msegments_latest_date()    FUNCTION     q  CREATE FUNCTION public.update_smotrim_msegments_latest_date() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
begin
for i in
select id from media_segments where relevant is true and smotrim_id is not null
loop
update media_segments set latest_episode_date = (select max(timestamp_aired) from smotrim_episodes where segment_id = i);
end loop;
end;
$$;
 =   DROP FUNCTION public.update_smotrim_msegments_latest_date();
       public          postgres    false    15            S           1255    917735    update_smotrim_segments_stats()    FUNCTION     n  CREATE FUNCTION public.update_smotrim_segments_stats() RETURNS void
    LANGUAGE plpgsql
    AS $$
begin
insert into service.media_segments_stats (segment_id, day_date, total, total_time, have, have_time, transcribed, transcribed_time)
select id, now()::date, ss.total_count, ss.total_duration, sh.total_count, sh.total_duration, ts.total_count, ts.total_duration
from media_segments
inner join lateral get_smotrim_segment_stats(id) ss on true
inner join lateral get_smotrim_segment_stats_h(id) sh on true
inner join lateral get_transcribed_stats(id) ts on true
where relevant is true and smotrim_id is not null;
end;
$$;
 6   DROP FUNCTION public.update_smotrim_segments_stats();
       public          postgres    false    15            T           1255    917736    update_tchannels_data()    FUNCTION     )  CREATE FUNCTION public.update_tchannels_data() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
begin
for i in
select id from telegram_channels where relevant is true
loop
update telegram_channels set history_count = get_tchannel_history_count(i) where id = i;
end loop;
end;
$$;
 .   DROP FUNCTION public.update_tchannels_data();
       public          postgres    false    15            U           1255    917737    update_updated_on()    FUNCTION     �   CREATE FUNCTION public.update_updated_on() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
NEW.updated_on = NOW();
RETURN NEW;
END;
$$;
 *   DROP FUNCTION public.update_updated_on();
       public          postgres    false    15            V           1255    917738 &   update_youtube_msegments_latest_date()    FUNCTION     �  CREATE FUNCTION public.update_youtube_msegments_latest_date() RETURNS void
    LANGUAGE plpgsql STRICT
    AS $$
declare
i int;
begin
for i in
select id from media_segments where relevant is true and (cluster = 'youtube' or cluster = 'zvezda')
loop
update media_segments set latest_episode_date = (select max(timestamp_aired) from youtube_vids where segment_id = i);
end loop;
end;
$$;
 =   DROP FUNCTION public.update_youtube_msegments_latest_date();
       public          postgres    false    15            W           1255    917739    update_youtube_segments_stats()    FUNCTION     �  CREATE FUNCTION public.update_youtube_segments_stats() RETURNS void
    LANGUAGE plpgsql
    AS $$
begin
insert into service.media_segments_stats (segment_id, day_date, total, total_time, have, have_time, transcribed, transcribed_time)
select id, now()::date, ys.total_count, ys.total_duration, yh.total_count, yh.total_duration, yt.total_count, yt.total_duration
from media_segments
inner join lateral get_youtube_segment_stats(id) ys on true
inner join lateral get_youtube_segment_stats_h(id) yh on true
inner join lateral get_transcribed_stats(id) yt on true
where relevant is true and cluster in ('youtube', 'zvezda', 'daytv', 'roytv');
end;
$$;
 6   DROP FUNCTION public.update_youtube_segments_stats();
       public          postgres    false    15            -           1259    917997 
   auth_group    TABLE     e   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap    postgres    false    15            .           1259    918000    auth_group_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    301    15            /           1259    918001    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap    postgres    false    15            0           1259    918004    auth_group_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    303            1           1259    918005    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap    postgres    false    15            2           1259    918008    auth_permission_id_seq    SEQUENCE     �   ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    305            3           1259    918009 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap    postgres    false    15            4           1259    918012    auth_user_groups    TABLE     ~   CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap    postgres    false    15            5           1259    918015    auth_user_groups_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    308    15            6           1259    918016    auth_user_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    307    15            7           1259    918017    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap    postgres    false    15            8           1259    918020 !   auth_user_user_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    311            9           1259    918021    days_of_war    TABLE     O   CREATE TABLE public.days_of_war (
    id bigint NOT NULL,
    day_date date
);
    DROP TABLE public.days_of_war;
       public         heap    postgres    false    15            <           0    0    TABLE days_of_war    COMMENT     X   COMMENT ON TABLE public.days_of_war IS 'Enumerator of days starting with Feb 24, 2022';
          public          postgres    false    313            :           1259    918024    days_of_war_id_seq    SEQUENCE     �   ALTER TABLE public.days_of_war ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.days_of_war_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    313            ;           1259    918025    dentv_episodes    TABLE     �  CREATE TABLE public.dentv_episodes (
    id bigint NOT NULL,
    title text,
    date_aired date,
    dentv_url text,
    direct_url text,
    description text,
    duration bigint,
    segment_id integer,
    stats jsonb,
    comments jsonb[],
    need boolean DEFAULT true,
    have boolean DEFAULT false,
    url_is_alive boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    youtube_rec_id integer,
    premium boolean DEFAULT false NOT NULL
);
 "   DROP TABLE public.dentv_episodes;
       public         heap    postgres    false    15            <           1259    918035    dentv_episodes_id_seq    SEQUENCE     �   ALTER TABLE public.dentv_episodes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.dentv_episodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    315    15            =           1259    918036    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap    postgres    false    15            >           1259    918042    django_admin_log_id_seq    SEQUENCE     �   ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    317    15            ?           1259    918043    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap    postgres    false    15            @           1259    918046    django_content_type_id_seq    SEQUENCE     �   ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    319            A           1259    918047    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap    postgres    false    15            B           1259    918052    django_migrations_id_seq    SEQUENCE     �   ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    321    15            C           1259    918053    komso_episodes    TABLE     z  CREATE TABLE public.komso_episodes (
    id integer NOT NULL,
    komso_id integer NOT NULL,
    komso_seq smallint,
    title text,
    description text,
    timestamp_aired timestamp with time zone,
    additional_data jsonb,
    duration bigint,
    segment_id integer,
    have boolean,
    need boolean,
    url_is_alive boolean,
    komso_url text,
    direct_url text
);
 "   DROP TABLE public.komso_episodes;
       public         heap    postgres    false    15            =           0    0    TABLE komso_episodes    COMMENT     n   COMMENT ON TABLE public.komso_episodes IS 'Episodes of the Komsomolskaya Pravda (Komsomolka) media network ';
          public          postgres    false    323            >           0    0    COLUMN komso_episodes.komso_id    COMMENT     Y   COMMENT ON COLUMN public.komso_episodes.komso_id IS 'Int. Unique komsomolka identifier';
          public          postgres    false    323            ?           0    0    COLUMN komso_episodes.komso_seq    COMMENT     i   COMMENT ON COLUMN public.komso_episodes.komso_seq IS 'Int. Sequence of episode within a segment''s set';
          public          postgres    false    323            @           0    0    COLUMN komso_episodes.title    COMMENT     K   COMMENT ON COLUMN public.komso_episodes.title IS 'String. Original title';
          public          postgres    false    323            A           0    0 %   COLUMN komso_episodes.additional_data    COMMENT     y   COMMENT ON COLUMN public.komso_episodes.additional_data IS 'JSON. Catchall field to store other possibly relevant data';
          public          postgres    false    323            B           0    0    COLUMN komso_episodes.duration    COMMENT     G   COMMENT ON COLUMN public.komso_episodes.duration IS 'Int. In seconds';
          public          postgres    false    323            C           0    0    COLUMN komso_episodes.have    COMMENT     X   COMMENT ON COLUMN public.komso_episodes.have IS 'Bool. True if episode was downloaded';
          public          postgres    false    323            D           0    0    COLUMN komso_episodes.need    COMMENT     Z   COMMENT ON COLUMN public.komso_episodes.need IS 'Bool. False if episode is not relevant';
          public          postgres    false    323            E           0    0 "   COLUMN komso_episodes.url_is_alive    COMMENT     i   COMMENT ON COLUMN public.komso_episodes.url_is_alive IS 'Bool. False if download failed too many times';
          public          postgres    false    323            F           0    0    COLUMN komso_episodes.komso_url    COMMENT     t   COMMENT ON COLUMN public.komso_episodes.komso_url IS 'String. URL of the episode on the public komsomolka website';
          public          postgres    false    323            G           0    0     COLUMN komso_episodes.direct_url    COMMENT     ^   COMMENT ON COLUMN public.komso_episodes.direct_url IS 'String. URL to episode''s audio file';
          public          postgres    false    323            D           1259    918058    komso_episodes_id_seq    SEQUENCE     �   ALTER TABLE public.komso_episodes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.komso_episodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    323            E           1259    918059    localities_by_region    VIEW     ,  CREATE VIEW public.localities_by_region AS
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
 '   DROP VIEW public.localities_by_region;
       public          postgres    false    15            F           1259    918064    media_coverage_type    TABLE     a   CREATE TABLE public.media_coverage_type (
    id bigint NOT NULL,
    type_name text NOT NULL
);
 '   DROP TABLE public.media_coverage_type;
       public         heap    postgres    false    15            H           0    0    TABLE media_coverage_type    COMMENT     U   COMMENT ON TABLE public.media_coverage_type IS 'Enumerator of media coverage types';
          public          postgres    false    326            G           1259    918069    media_roles    TABLE     d   CREATE TABLE public.media_roles (
    id bigint NOT NULL,
    role text NOT NULL,
    notes text
);
    DROP TABLE public.media_roles;
       public         heap    postgres    false    15            I           0    0    TABLE media_roles    COMMENT     \   COMMENT ON TABLE public.media_roles IS 'Enumerator of possible roles in media environment';
          public          postgres    false    327            H           1259    918074    media_segments    TABLE       CREATE TABLE public.media_segments (
    id integer NOT NULL,
    name_ru text,
    parent_org_id bigint,
    avg_guest_time smallint,
    name_en text,
    smotrim_id integer,
    cluster text,
    relevant boolean DEFAULT true,
    name_uk text,
    is_defunct boolean DEFAULT false NOT NULL,
    segment_type text,
    duration_threashold integer,
    latest_episode_date timestamp with time zone,
    komso_id integer,
    rutube_id text,
    ntv_id jsonb,
    description text,
    updated_on timestamp with time zone
);
 "   DROP TABLE public.media_segments;
       public         heap    postgres    false    15            J           0    0    TABLE media_segments    COMMENT     P   COMMENT ON TABLE public.media_segments IS 'Enumerator of known media segments';
          public          postgres    false    328            K           0    0    COLUMN media_segments.name_ru    COMMENT     [   COMMENT ON COLUMN public.media_segments.name_ru IS 'String. Original name of the segment';
          public          postgres    false    328            L           0    0 #   COLUMN media_segments.parent_org_id    COMMENT     r   COMMENT ON COLUMN public.media_segments.parent_org_id IS 'Present if segment is a spawn of a known organization';
          public          postgres    false    328            M           0    0 $   COLUMN media_segments.avg_guest_time    COMMENT     {   COMMENT ON COLUMN public.media_segments.avg_guest_time IS 'Int. EXPERIMENTAL. Shows approximate presense time in minutes';
          public          postgres    false    328            N           0    0     COLUMN media_segments.smotrim_id    COMMENT     [   COMMENT ON COLUMN public.media_segments.smotrim_id IS 'Int. Unique Smotrim.ru identifier';
          public          postgres    false    328            O           0    0    COLUMN media_segments.cluster    COMMENT     �   COMMENT ON COLUMN public.media_segments.cluster IS 'String. Logical clusters, usually a derivative of a channel name. Could be sololive, vesti, zvezda, komso';
          public          postgres    false    328            P           0    0    COLUMN media_segments.relevant    COMMENT     r   COMMENT ON COLUMN public.media_segments.relevant IS 'Bool. True if segment should be displayed in the W web app';
          public          postgres    false    328            Q           0    0     COLUMN media_segments.is_defunct    COMMENT     n   COMMENT ON COLUMN public.media_segments.is_defunct IS 'Bool. True if media segment is no longer in rotation';
          public          postgres    false    328            R           0    0 "   COLUMN media_segments.segment_type    COMMENT     j   COMMENT ON COLUMN public.media_segments.segment_type IS 'String. Can be ''titled'', `synthetic` or null';
          public          postgres    false    328            S           0    0 )   COLUMN media_segments.duration_threashold    COMMENT     x   COMMENT ON COLUMN public.media_segments.duration_threashold IS 'Int. Indicates the minimal value for episode duration';
          public          postgres    false    328            T           0    0    COLUMN media_segments.komso_id    COMMENT     Y   COMMENT ON COLUMN public.media_segments.komso_id IS 'Int. Unique komsomolka identifier';
          public          postgres    false    328            U           0    0    COLUMN media_segments.rutube_id    COMMENT     ]   COMMENT ON COLUMN public.media_segments.rutube_id IS 'Table rutube_vids doesn''t exist yet';
          public          postgres    false    328            V           0    0    COLUMN media_segments.ntv_id    COMMENT     j   COMMENT ON COLUMN public.media_segments.ntv_id IS 'JSONB. Composite identifier with ntv_id and ntv_slug';
          public          postgres    false    328            I           1259    918081    media_segments_id_seq    SEQUENCE     �   ALTER TABLE public.media_segments ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.media_segments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    328    15            �           1259    1834345    msegments_extended    VIEW     �  CREATE VIEW public.msegments_extended AS
SELECT
    NULL::text AS name_ru,
    NULL::text AS name_en,
    NULL::text AS name_uk,
    NULL::text AS cluster,
    NULL::text AS segment_type,
    NULL::timestamp with time zone AS latest_episode_date,
    NULL::text AS parent_org,
    NULL::integer AS total,
    NULL::double precision AS total_time,
    NULL::integer AS transcribed,
    NULL::double precision AS transcribed_time,
    NULL::integer AS have,
    NULL::double precision AS have_time;
 %   DROP VIEW public.msegments_extended;
       public          postgres    false    15            J           1259    918086    msegments_to_rchannels_mapping    TABLE     �   CREATE TABLE public.msegments_to_rchannels_mapping (
    id bigint NOT NULL,
    rutube_channel_id integer,
    media_segment_id bigint
);
 2   DROP TABLE public.msegments_to_rchannels_mapping;
       public         heap    postgres    false    15            W           0    0 $   TABLE msegments_to_rchannels_mapping    COMMENT     p   COMMENT ON TABLE public.msegments_to_rchannels_mapping IS 'Mapping between media_segments and rutube_channels';
          public          postgres    false    330            K           1259    918089 %   msegments_to_rchannels_mapping_id_seq    SEQUENCE     �   ALTER TABLE public.msegments_to_rchannels_mapping ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.msegments_to_rchannels_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    330            L           1259    918090    msegments_to_ychannels_mapping    TABLE     �   CREATE TABLE public.msegments_to_ychannels_mapping (
    id bigint NOT NULL,
    youtube_channel_id bigint,
    media_segment_id bigint
);
 2   DROP TABLE public.msegments_to_ychannels_mapping;
       public         heap    postgres    false    15            X           0    0 $   TABLE msegments_to_ychannels_mapping    COMMENT     q   COMMENT ON TABLE public.msegments_to_ychannels_mapping IS 'Mapping between media_segments and youtube_channels';
          public          postgres    false    332            M           1259    918093 %   msegments_to_ychannels_mapping_id_seq    SEQUENCE     �   ALTER TABLE public.msegments_to_ychannels_mapping ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.msegments_to_ychannels_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    332    15            N           1259    918094    ntv_episodes    TABLE     �  CREATE TABLE public.ntv_episodes (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    title text,
    description text,
    segment_id integer,
    timestamp_aired timestamp with time zone,
    views integer,
    timeline jsonb,
    ntv_id integer NOT NULL,
    need boolean DEFAULT true NOT NULL,
    have boolean DEFAULT false NOT NULL,
    url_is_alive boolean DEFAULT true NOT NULL,
    duration integer,
    rutube_id text
);
     DROP TABLE public.ntv_episodes;
       public         heap    postgres    false    15            Y           0    0    COLUMN ntv_episodes.title    COMMENT     I   COMMENT ON COLUMN public.ntv_episodes.title IS 'String. Original title';
          public          postgres    false    334            Z           0    0    COLUMN ntv_episodes.description    COMMENT     g   COMMENT ON COLUMN public.ntv_episodes.description IS 'String. Must be present if `timeline'' is null';
          public          postgres    false    334            [           0    0    COLUMN ntv_episodes.views    COMMENT     _   COMMENT ON COLUMN public.ntv_episodes.views IS 'Int. Number of views at the time of scraping';
          public          postgres    false    334            \           0    0    COLUMN ntv_episodes.timeline    COMMENT     �   COMMENT ON COLUMN public.ntv_episodes.timeline IS 'JSONB. Cotains same data as `description'' but with timestamps and split into several records';
          public          postgres    false    334            ]           0    0    COLUMN ntv_episodes.ntv_id    COMMENT     [   COMMENT ON COLUMN public.ntv_episodes.ntv_id IS 'Int. Internal NTV identifier fora video';
          public          postgres    false    334            ^           0    0    COLUMN ntv_episodes.duration    COMMENT     �   COMMENT ON COLUMN public.ntv_episodes.duration IS 'Int. Not present in the initial data; if null, it means video was not downloaded';
          public          postgres    false    334            O           1259    918103    ntv_episodes_id_seq    SEQUENCE     �   ALTER TABLE public.ntv_episodes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.ntv_episodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    334            P           1259    918104 !   organization_coverage_type_id_seq    SEQUENCE     �   ALTER TABLE public.media_coverage_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.organization_coverage_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    326            Q           1259    918105    organization_type    TABLE     |   CREATE TABLE public.organization_type (
    id bigint NOT NULL,
    org_type text,
    parent_type bigint,
    note text
);
 %   DROP TABLE public.organization_type;
       public         heap    postgres    false    15            _           0    0    TABLE organization_type    COMMENT     �   COMMENT ON TABLE public.organization_type IS 'Categorization by type. Type "holding" may contain other entities, including other holdings';
          public          postgres    false    337            R           1259    918110    organization_type_id_seq    SEQUENCE     �   ALTER TABLE public.organization_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.organization_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    337    15            S           1259    918111    organizations    TABLE     �  CREATE TABLE public.organizations (
    id bigint NOT NULL,
    name_en text,
    name_ru text,
    parent_org_id bigint,
    region bigint,
    source_url text,
    org_type_id bigint,
    coverage_type_id bigint,
    short_name jsonb,
    name_uk text,
    state_affiliated boolean,
    org_form_raw text,
    org_form jsonb,
    international boolean DEFAULT false,
    relevant boolean NOT NULL,
    org_type bigint,
    updated_on timestamp with time zone
);
 !   DROP TABLE public.organizations;
       public         heap    postgres    false    15            `           0    0    TABLE organizations    COMMENT     o   COMMENT ON TABLE public.organizations IS 'Organizations with which propagandists are or have been associated';
          public          postgres    false    339            a           0    0    COLUMN organizations.name_en    COMMENT     �   COMMENT ON COLUMN public.organizations.name_en IS 'String. Name of the org in English transliteration, or original if org has a latinized name';
          public          postgres    false    339            b           0    0    COLUMN organizations.name_ru    COMMENT     �   COMMENT ON COLUMN public.organizations.name_ru IS 'String. Name of the org in Russian transliteration, or original if org is Russian or has latinized name';
          public          postgres    false    339            c           0    0 "   COLUMN organizations.parent_org_id    COMMENT     �   COMMENT ON COLUMN public.organizations.parent_org_id IS 'Int. Internal reference; present if organization`s parent is known and present in the DB';
          public          postgres    false    339            d           0    0    COLUMN organizations.region    COMMENT     E   COMMENT ON COLUMN public.organizations.region IS 'TO BE DEPRECATED';
          public          postgres    false    339            e           0    0    COLUMN organizations.source_url    COMMENT     _   COMMENT ON COLUMN public.organizations.source_url IS 'complete only if org is a media source';
          public          postgres    false    339            f           0    0     COLUMN organizations.org_type_id    COMMENT     J   COMMENT ON COLUMN public.organizations.org_type_id IS 'TO BE DEPRECATED';
          public          postgres    false    339            g           0    0    COLUMN organizations.short_name    COMMENT     �   COMMENT ON COLUMN public.organizations.short_name IS 'JSONB. Abbreviation or short version of org`s name in the tripple language format';
          public          postgres    false    339            h           0    0    COLUMN organizations.name_uk    COMMENT     �   COMMENT ON COLUMN public.organizations.name_uk IS 'String. Name of the org in Ukrainian transliteration, or original if org is Ukrainian or has latinized name';
          public          postgres    false    339            i           0    0 %   COLUMN organizations.state_affiliated    COMMENT     �   COMMENT ON COLUMN public.organizations.state_affiliated IS 'Bool. True if affiliated with state but not a governmental agency';
          public          postgres    false    339            j           0    0 !   COLUMN organizations.org_form_raw    COMMENT     ]   COMMENT ON COLUMN public.organizations.org_form_raw IS 'String. Org`s form raw description';
          public          postgres    false    339            k           0    0    COLUMN organizations.org_form    COMMENT     x   COMMENT ON COLUMN public.organizations.org_form IS 'JSONB. Org`s organizational format in the tripple language format';
          public          postgres    false    339            l           0    0 "   COLUMN organizations.international    COMMENT     f   COMMENT ON COLUMN public.organizations.international IS 'Bool. True if org operates internationally';
          public          postgres    false    339            m           0    0    COLUMN organizations.relevant    COMMENT     {   COMMENT ON COLUMN public.organizations.relevant IS 'Bool. Indicates if organization should be displayed in the W web app';
          public          postgres    false    339            n           0    0    COLUMN organizations.org_type    COMMENT     e   COMMENT ON COLUMN public.organizations.org_type IS 'This column is to support the new org taxonomy';
          public          postgres    false    339            T           1259    918117    organizations_id_seq    SEQUENCE     �   ALTER TABLE public.organizations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.organizations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    339            U           1259    918118    people    TABLE     �  CREATE TABLE public.people (
    fullname_en text NOT NULL,
    fullname_ru text NOT NULL,
    id integer NOT NULL,
    lastname_en text,
    lastname_ru text,
    is_onmap boolean DEFAULT false,
    social text[],
    dob date,
    is_ttu boolean,
    is_ff boolean,
    relevant boolean DEFAULT true NOT NULL,
    contact jsonb,
    address text[],
    associates jsonb[],
    additional jsonb,
    aliases jsonb[],
    info jsonb,
    dod date,
    cod character varying,
    known_for jsonb,
    wiki_ref jsonb,
    namesake_seq smallint DEFAULT '1'::smallint,
    fullname_uk text,
    added_on timestamp with time zone DEFAULT now() NOT NULL,
    sex text,
    updated_on timestamp with time zone
);
    DROP TABLE public.people;
       public         heap    postgres    false    15            o           0    0    TABLE people    COMMENT     ^   COMMENT ON TABLE public.people IS 'Basic information about Russian propaganda personalities';
          public          postgres    false    341            p           0    0    COLUMN people.fullname_en    COMMENT     �   COMMENT ON COLUMN public.people.fullname_en IS 'String. Full name of patient in English transliteration, or original if patient is foreigner. May include non-ascii characters';
          public          postgres    false    341            q           0    0    COLUMN people.fullname_ru    COMMENT     �   COMMENT ON COLUMN public.people.fullname_ru IS 'String. Full name of patient in Russian transliteration, or original if patient is of Russian/Ukrainian origin';
          public          postgres    false    341            r           0    0    COLUMN people.lastname_en    COMMENT     �   COMMENT ON COLUMN public.people.lastname_en IS 'String. Last name of patient in English transliteration; in most cases it is the last word from fullname_en';
          public          postgres    false    341            s           0    0    COLUMN people.lastname_ru    COMMENT     �   COMMENT ON COLUMN public.people.lastname_ru IS 'String. Last name of patient in Russian transliteration; in most cases it is the last word from fullname_ru';
          public          postgres    false    341            t           0    0    COLUMN people.is_onmap    COMMENT     U   COMMENT ON COLUMN public.people.is_onmap IS 'Bool. LEGACY: not used in the project';
          public          postgres    false    341            u           0    0    COLUMN people.social    COMMENT     `   COMMENT ON COLUMN public.people.social IS 'List of strings. URLs to patient`s social networks';
          public          postgres    false    341            v           0    0    COLUMN people.dob    COMMENT     H   COMMENT ON COLUMN public.people.dob IS 'Date. Patient`s date of birth';
          public          postgres    false    341            w           0    0    COLUMN people.is_ttu    COMMENT     d   COMMENT ON COLUMN public.people.is_ttu IS 'Bool. Indicates if the patient is a traitor to Ukraine';
          public          postgres    false    341            x           0    0    COLUMN people.is_ff    COMMENT     q   COMMENT ON COLUMN public.people.is_ff IS 'Bool. Indicates if the patient is a Putin`s ally from without Russia';
          public          postgres    false    341            y           0    0    COLUMN people.relevant    COMMENT     s   COMMENT ON COLUMN public.people.relevant IS 'Bool. Indicates if the patient should be displayed in the W web app';
          public          postgres    false    341            z           0    0    COLUMN people.contact    COMMENT     �   COMMENT ON COLUMN public.people.contact IS 'JSONB. Contains patient`s contact information. Possible keys are emails, phones, telegram. Values are lists of strings';
          public          postgres    false    341            {           0    0    COLUMN people.address    COMMENT     �   COMMENT ON COLUMN public.people.address IS 'List of strings. Contains patient`s possible addresses. Values are NOT normalized';
          public          postgres    false    341            |           0    0    COLUMN people.associates    COMMENT     c  COMMENT ON COLUMN public.people.associates IS 'List of JSONB. Contains patient`s known associates such as spouses, children, parents, colleagues etc. Each item contains some of the keys present in this table as columns. Mandatory keys are relationship and whatever identifies the associate, which can be either name or id if associate is also a patient';
          public          postgres    false    341            }           0    0    COLUMN people.additional    COMMENT     �   COMMENT ON COLUMN public.people.additional IS 'JSONB. Contains other relevant information about the patient. Most common keys are passport (json with passport details), urls (list of links), tin (string)';
          public          postgres    false    341            ~           0    0    COLUMN people.aliases    COMMENT     �   COMMENT ON COLUMN public.people.aliases IS 'List of JSONB. Contains patient`s aliases, maiden names, nicknames etc in the tripple language format';
          public          postgres    false    341                       0    0    COLUMN people.info    COMMENT     6   COMMENT ON COLUMN public.people.info IS 'JSONB. WIP';
          public          postgres    false    341            �           0    0    COLUMN people.dod    COMMENT     H   COMMENT ON COLUMN public.people.dod IS 'Date. Patient`s date of death';
          public          postgres    false    341            �           0    0    COLUMN people.cod    COMMENT     K   COMMENT ON COLUMN public.people.cod IS 'String. Patient`s cause of death';
          public          postgres    false    341            �           0    0    COLUMN people.known_for    COMMENT     y   COMMENT ON COLUMN public.people.known_for IS 'JSONB. Single-line summary of the patient in the tripple language format';
          public          postgres    false    341            �           0    0    COLUMN people.wiki_ref    COMMENT     �   COMMENT ON COLUMN public.people.wiki_ref IS 'JSONB. URLs to Wikipedia articles about the patient. Keys are 2-letter language code, values are URLs';
          public          postgres    false    341            �           0    0    COLUMN people.namesake_seq    COMMENT     �   COMMENT ON COLUMN public.people.namesake_seq IS 'Int. Part of the table identity. Indicates patient`s order in the namesakes list. Was introduced to handle patients with identical names';
          public          postgres    false    341            �           0    0    COLUMN people.fullname_uk    COMMENT     �   COMMENT ON COLUMN public.people.fullname_uk IS 'String. Full name of patient in Ukrainian transliteration, or original if patient is of Ukrainian origin';
          public          postgres    false    341            V           1259    918127    people_in_orgs    TABLE     l  CREATE TABLE public.people_in_orgs (
    id bigint NOT NULL,
    person_id integer NOT NULL,
    org_id bigint NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    notes text,
    is_in_control boolean DEFAULT false,
    role jsonb,
    year_started smallint,
    year_ended smallint,
    role_category bigint,
    role_ref bigint,
    role_details jsonb
);
 "   DROP TABLE public.people_in_orgs;
       public         heap    postgres    false    15            �           0    0    TABLE people_in_orgs    COMMENT     �   COMMENT ON TABLE public.people_in_orgs IS 'Relationships between organizations and people. Primary key is (person_id, org_id, is_active, role). New recs must have all of these defined';
          public          postgres    false    342            �           0    0    COLUMN people_in_orgs.is_active    COMMENT     b   COMMENT ON COLUMN public.people_in_orgs.is_active IS 'Bool. True if the relationship is ongoing';
          public          postgres    false    342            �           0    0    COLUMN people_in_orgs.role    COMMENT     �   COMMENT ON COLUMN public.people_in_orgs.role IS 'JSONB. Description of the patient`s role in the organization in tripple language format';
          public          postgres    false    342            �           0    0 #   COLUMN people_in_orgs.role_category    COMMENT     Z   COMMENT ON COLUMN public.people_in_orgs.role_category IS 'Reference to ISCO-08 taxonomy';
          public          postgres    false    342            W           1259    918134    orgs_extended    VIEW     �  CREATE VIEW public.orgs_extended AS
 SELECT o.id,
    o.name_ru,
    o.name_en,
    o.name_uk,
    o.short_name,
    otax.term AS org_type,
    public.get_organization_ancestors(o.id) AS parent_orgs,
    o.source_url,
    o.state_affiliated,
    public.get_org_people(o.id) AS ppl
   FROM (((public.organizations o
     LEFT JOIN public.people_in_orgs pio ON ((o.id = pio.org_id)))
     LEFT JOIN enums.orgs_taxonomy otax ON ((o.org_type = otax.id)))
     LEFT JOIN public.people p ON ((p.id = pio.person_id)))
  WHERE (o.relevant IS TRUE)
  GROUP BY o.name_ru, o.name_en, o.name_uk, o.source_url, o.short_name, o.state_affiliated, o.org_form, otax.term, o.id
  ORDER BY o.name_ru;
     DROP VIEW public.orgs_extended;
       public          postgres    false    341    533    534    339    339    339    339    342    342    339    339    339    339    339    339    15            X           1259    918139    people_3rdprt_details_raw    TABLE     �   CREATE TABLE public.people_3rdprt_details_raw (
    id bigint NOT NULL,
    person_id integer NOT NULL,
    url text NOT NULL,
    text_raw text
);
 -   DROP TABLE public.people_3rdprt_details_raw;
       public         heap    postgres    false    15            �           0    0    TABLE people_3rdprt_details_raw    COMMENT     k   COMMENT ON TABLE public.people_3rdprt_details_raw IS 'Links to and extracted text from 3rd party sources';
          public          postgres    false    344            Y           1259    918144     people_3rdprt_details_raw_id_seq    SEQUENCE     �   ALTER TABLE public.people_3rdprt_details_raw ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_3rdprt_details_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    344    15            Z           1259    918145    people_bundles    TABLE     �   CREATE TABLE public.people_bundles (
    id bigint NOT NULL,
    bundle_name jsonb,
    parent_bundle_id bigint,
    description text,
    bundle_type bigint
);
 "   DROP TABLE public.people_bundles;
       public         heap    postgres    false    15            �           0    0    TABLE people_bundles    COMMENT     L   COMMENT ON TABLE public.people_bundles IS 'Custom groups of personalities';
          public          postgres    false    346            �           0    0 !   COLUMN people_bundles.bundle_name    COMMENT     o   COMMENT ON COLUMN public.people_bundles.bundle_name IS 'JSONB. Name of the bundle in tripple language format';
          public          postgres    false    346            [           1259    918150    people_bundles_id_seq    SEQUENCE     �   ALTER TABLE public.people_bundles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_bundles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    346    15            �           1259    2582504    people_extended    VIEW     _  CREATE VIEW public.people_extended AS
SELECT
    NULL::integer AS id,
    NULL::text AS fullname_uk,
    NULL::text AS fullname_ru,
    NULL::text AS fullname_en,
    NULL::text AS lastname_en,
    NULL::text AS lastname_ru,
    NULL::text[] AS social,
    NULL::date AS dob,
    NULL::jsonb AS contact,
    NULL::text[] AS address,
    NULL::jsonb[] AS associates,
    NULL::jsonb AS additional,
    NULL::jsonb[] AS aliases,
    NULL::jsonb AS info,
    NULL::date AS dod,
    NULL::character varying AS cod,
    NULL::jsonb AS known_for,
    NULL::jsonb AS wiki_ref,
    NULL::text AS photo,
    NULL::text[] AS external_links,
    NULL::jsonb[] AS bundles,
    NULL::text AS thumb,
    NULL::timestamp with time zone AS added_on,
    NULL::jsonb[] AS orgs,
    NULL::text AS sex,
    NULL::jsonb[] AS telegram_channels,
    NULL::jsonb[] AS youtube_channels;
 "   DROP VIEW public.people_extended;
       public          postgres    false    15            �           0    0    TABLE people_extended    ACL     8   GRANT ALL ON TABLE public.people_extended TO windmill2;
          public          postgres    false    410            \           1259    918155    people_in_bundles    TABLE     �   CREATE TABLE public.people_in_bundles (
    id bigint NOT NULL,
    person_id integer NOT NULL,
    bundle_id bigint NOT NULL
);
 %   DROP TABLE public.people_in_bundles;
       public         heap    postgres    false    15            �           0    0    TABLE people_in_bundles    COMMENT     Z   COMMENT ON TABLE public.people_in_bundles IS 'Mapping between people and people_bundles';
          public          postgres    false    348            ]           1259    918158    people_in_bundles_id_seq    SEQUENCE     �   ALTER TABLE public.people_in_bundles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_in_bundles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    348    15            ^           1259    918159    people_in_orgs_id_seq    SEQUENCE     �   ALTER TABLE public.people_in_orgs ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_in_orgs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    342            _           1259    918160    people_in_ur    TABLE     �  CREATE TABLE public.people_in_ur (
    id integer NOT NULL,
    in_higher_council boolean,
    in_higher_council_bureau boolean,
    in_general_council boolean,
    in_general_council_presidium boolean,
    in_general_council_presidium_commission boolean,
    in_central_executive_committee boolean,
    is_gosduma_deputy boolean,
    is_senator boolean,
    in_ethics_commission boolean,
    in_coordination_councils_leadership boolean,
    in_central_fans_council boolean,
    in_central_control_commission boolean,
    in_international_aff_commission boolean,
    url text,
    ur_text text,
    is_secretary boolean,
    person_id integer NOT NULL
);
     DROP TABLE public.people_in_ur;
       public         heap    postgres    false    15            �           0    0    TABLE people_in_ur    COMMENT     j   COMMENT ON TABLE public.people_in_ur IS 'Members of the United Russia (Edinaya Rossiya) political party';
          public          postgres    false    351            `           1259    918165    people_in_ur_id_seq    SEQUENCE     �   ALTER TABLE public.people_in_ur ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_in_ur_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    351    15            a           1259    918166    people_on_photos    TABLE     �   CREATE TABLE public.people_on_photos (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    person_id integer NOT NULL,
    photo_id bigint NOT NULL
);
 $   DROP TABLE public.people_on_photos;
       public         heap    postgres    false    15            �           0    0    TABLE people_on_photos    COMMENT     Q   COMMENT ON TABLE public.people_on_photos IS 'Mapping between people and photos';
          public          postgres    false    353            b           1259    918170    people_on_photos_id_seq    SEQUENCE     �   ALTER TABLE public.people_on_photos ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_on_photos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    353    15            c           1259    918171    people_on_smotrim    TABLE     �   CREATE TABLE public.people_on_smotrim (
    id bigint NOT NULL,
    person_id integer NOT NULL,
    episode_id integer NOT NULL,
    media_role_id bigint NOT NULL
);
 %   DROP TABLE public.people_on_smotrim;
       public         heap    postgres    false    15            �           0    0    TABLE people_on_smotrim    COMMENT     \   COMMENT ON TABLE public.people_on_smotrim IS 'Mapping between people and smotrim_episodes';
          public          postgres    false    355            d           1259    918174    people_on_smotrim_id_seq    SEQUENCE     �   ALTER TABLE public.people_on_smotrim ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_on_smotrim_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    355            e           1259    918175    people_on_youtube    TABLE     �   CREATE TABLE public.people_on_youtube (
    id bigint NOT NULL,
    person_id integer,
    episode_id integer,
    media_role_id bigint
);
 %   DROP TABLE public.people_on_youtube;
       public         heap    postgres    false    15            �           0    0    TABLE people_on_youtube    COMMENT     X   COMMENT ON TABLE public.people_on_youtube IS 'Mapping between people and youtube_vids';
          public          postgres    false    357            f           1259    918178    people_on_youtube_id_seq    SEQUENCE     �   ALTER TABLE public.people_on_youtube ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_on_youtube_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    357    15            g           1259    918179    people_to_msegments_mapping    TABLE     �   CREATE TABLE public.people_to_msegments_mapping (
    id bigint NOT NULL,
    person_id integer,
    media_segment_id integer
);
 /   DROP TABLE public.people_to_msegments_mapping;
       public         heap    postgres    false    15            �           0    0 !   TABLE people_to_msegments_mapping    COMMENT     d   COMMENT ON TABLE public.people_to_msegments_mapping IS 'Mapping between people and media_segments';
          public          postgres    false    359            h           1259    918182 "   people_to_msegments_mapping_id_seq    SEQUENCE     �   ALTER TABLE public.people_to_msegments_mapping ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.people_to_msegments_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    359            i           1259    918183    person_id_seq    SEQUENCE     �   ALTER TABLE public.people ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    341            j           1259    918184    person_media_role_id_seq    SEQUENCE     �   ALTER TABLE public.media_roles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.person_media_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    327    15            k           1259    918185    photos    TABLE     �   CREATE TABLE public.photos (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    url text,
    is_face boolean,
    type text
);
    DROP TABLE public.photos;
       public         heap    postgres    false    15            �           0    0    COLUMN photos.url    COMMENT     ?   COMMENT ON COLUMN public.photos.url IS 'String. Complete URL';
          public          postgres    false    363            �           0    0    COLUMN photos.is_face    COMMENT     j   COMMENT ON COLUMN public.photos.is_face IS 'Bool. Indicates if the photo is used as a patient face in W';
          public          postgres    false    363            �           0    0    COLUMN photos.type    COMMENT     I   COMMENT ON COLUMN public.photos.type IS 'String. Can be thumb or large';
          public          postgres    false    363            l           1259    918191    photos_id_seq    SEQUENCE     �   ALTER TABLE public.photos ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.photos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    363            m           1259    918192    printed    TABLE     %  CREATE TABLE public.printed (
    id bigint NOT NULL,
    title_ru text,
    title_en text,
    title_uk text,
    relevant boolean,
    type text,
    year smallint,
    description text,
    file_details jsonb,
    metadata jsonb,
    slug text,
    storage_ref uuid,
    int_review text
);
    DROP TABLE public.printed;
       public         heap    postgres    false    15            �           0    0    TABLE printed    COMMENT     7   COMMENT ON TABLE public.printed IS 'Books & articles';
          public          postgres    false    365            �           0    0    COLUMN printed.title_ru    COMMENT     [   COMMENT ON COLUMN public.printed.title_ru IS 'String. Original title of the printed item';
          public          postgres    false    365            �           0    0    COLUMN printed.year    COMMENT     D   COMMENT ON COLUMN public.printed.year IS 'Int. Year of publishing';
          public          postgres    false    365            �           0    0    COLUMN printed.file_details    COMMENT        COMMENT ON COLUMN public.printed.file_details IS 'JSON. Basic data on the original file, such as extention and size in bytes';
          public          postgres    false    365            �           0    0    COLUMN printed.metadata    COMMENT     U   COMMENT ON COLUMN public.printed.metadata IS 'JSON. Various metadata, such as ISBN';
          public          postgres    false    365            �           0    0    COLUMN printed.slug    COMMENT     Z   COMMENT ON COLUMN public.printed.slug IS 'String. Transliterated and slugified title_ru';
          public          postgres    false    365            �           0    0    COLUMN printed.storage_ref    COMMENT     �   COMMENT ON COLUMN public.printed.storage_ref IS 'UUID. Link to the record in the Storage reference table that is linked to the respective Storage object';
          public          postgres    false    365            n           1259    918197    printed_id_seq    SEQUENCE     �   ALTER TABLE public.printed ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.printed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    365    15            o           1259    918198    printed_to_people_mapping    TABLE     �   CREATE TABLE public.printed_to_people_mapping (
    id bigint NOT NULL,
    person_id integer,
    person_raw text,
    printed_id bigint NOT NULL,
    printed_piece_id bigint
);
 -   DROP TABLE public.printed_to_people_mapping;
       public         heap    postgres    false    15            �           0    0    TABLE printed_to_people_mapping    COMMENT     [   COMMENT ON TABLE public.printed_to_people_mapping IS 'Mapping between people and printed';
          public          postgres    false    367            p           1259    918203     printed_to_people_mapping_id_seq    SEQUENCE     �   ALTER TABLE public.printed_to_people_mapping ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.printed_to_people_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    367    15            q           1259    918204    quotes    TABLE     �   CREATE TABLE public.quotes (
    id bigint NOT NULL,
    person_id integer,
    content jsonb NOT NULL,
    source_id bigint,
    source_url text,
    date date
);
    DROP TABLE public.quotes;
       public         heap    postgres    false    15            r           1259    918209    quotes_id_seq    SEQUENCE     �   ALTER TABLE public.quotes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.quotes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    369            s           1259    918210    rutube_channels    TABLE     �   CREATE TABLE public.rutube_channels (
    id integer NOT NULL,
    name text,
    rutube_channel_id text,
    rutube_channel_alias text
);
 #   DROP TABLE public.rutube_channels;
       public         heap    postgres    false    15            �           0    0    TABLE rutube_channels    COMMENT     S   COMMENT ON TABLE public.rutube_channels IS 'Relevant channels on Rutube platform';
          public          postgres    false    371            t           1259    918215    rutube_channels_id_seq    SEQUENCE     �   ALTER TABLE public.rutube_channels ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.rutube_channels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    371    15            u           1259    918216    rutube_vids    TABLE     �   CREATE TABLE public.rutube_vids (
    id bigint NOT NULL,
    title text,
    rutube_id text,
    rutube_channel_id integer,
    media_segment_id integer
);
    DROP TABLE public.rutube_vids;
       public         heap    postgres    false    15            �           0    0    TABLE rutube_vids    COMMENT     L   COMMENT ON TABLE public.rutube_vids IS 'Episodes from the Rutube platform';
          public          postgres    false    373            v           1259    918221    rutube_vids_id_seq    SEQUENCE     �   ALTER TABLE public.rutube_vids ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.rutube_vids_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    373            w           1259    918222    smotrim_episodes    TABLE     F  CREATE TABLE public.smotrim_episodes (
    title text,
    timestamp_aired timestamp without time zone,
    id integer NOT NULL,
    smotrim_id text,
    segment_id integer,
    duration bigint,
    description text,
    have boolean DEFAULT false NOT NULL,
    url_is_alive boolean DEFAULT true NOT NULL,
    need boolean
);
 $   DROP TABLE public.smotrim_episodes;
       public         heap    postgres    false    15            �           0    0    TABLE smotrim_episodes    COMMENT     a   COMMENT ON TABLE public.smotrim_episodes IS 'Episodes of the Smotrim.ru media platform (VGTRK)';
          public          postgres    false    375            �           0    0 "   COLUMN smotrim_episodes.smotrim_id    COMMENT     `   COMMENT ON COLUMN public.smotrim_episodes.smotrim_id IS 'String. Unique Smotrim.ru identifier';
          public          postgres    false    375            �           0    0     COLUMN smotrim_episodes.duration    COMMENT     a   COMMENT ON COLUMN public.smotrim_episodes.duration IS 'Int. Duration of the episode in seconds';
          public          postgres    false    375            �           0    0    COLUMN smotrim_episodes.have    COMMENT     t   COMMENT ON COLUMN public.smotrim_episodes.have IS 'Bool. Indicate if video or audio of the episode was downloaded';
          public          postgres    false    375            �           0    0 $   COLUMN smotrim_episodes.url_is_alive    COMMENT     {   COMMENT ON COLUMN public.smotrim_episodes.url_is_alive IS 'Bool. Indicates if the URL worked when download was attempted';
          public          postgres    false    375            x           1259    918229    smotrim_episodes_id_seq    SEQUENCE     �   ALTER TABLE public.smotrim_episodes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.smotrim_episodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    375    15            y           1259    918230    telegram_authors    TABLE     �   CREATE TABLE public.telegram_authors (
    id bigint NOT NULL,
    person_id integer NOT NULL,
    channel_id integer NOT NULL
);
 $   DROP TABLE public.telegram_authors;
       public         heap    postgres    false    15            �           0    0    TABLE telegram_authors    COMMENT     a   COMMENT ON TABLE public.telegram_authors IS 'Relationship between people and telegram_channels';
          public          postgres    false    377            �           0    0    TABLE telegram_authors    ACL     9   GRANT ALL ON TABLE public.telegram_authors TO teledummy;
          public          postgres    false    377            z           1259    918233    telegram_authors_id_seq    SEQUENCE     �   ALTER TABLE public.telegram_authors ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.telegram_authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    377    15            {           1259    918234    telegram_channels    TABLE     /  CREATE TABLE public.telegram_channels (
    id integer NOT NULL,
    title text,
    telemetr_id text,
    telemetr_url text,
    relevant boolean DEFAULT true,
    population bigint,
    population_checked_on timestamp with time zone,
    handle text,
    date_created timestamp without time zone,
    status boolean DEFAULT true NOT NULL,
    origin_id bigint,
    description text,
    is_restricted boolean,
    is_fake boolean,
    is_scam boolean,
    no_forward boolean,
    restrictions jsonb[],
    linked_chat_id bigint,
    history_count bigint
);
 %   DROP TABLE public.telegram_channels;
       public         heap    postgres    false    15            �           0    0    TABLE telegram_channels    COMMENT       COMMENT ON TABLE public.telegram_channels IS 'Basic information about Telegram channels maintained by Russian propaganda personalities or otherwise connected to Russian propaganda.Column ''url'' is a ''t.me''-like URLColumn ''telemetr_id'' is ID of the channel in Telemetr';
          public          postgres    false    379            �           0    0 $   COLUMN telegram_channels.telemetr_id    COMMENT     q   COMMENT ON COLUMN public.telegram_channels.telemetr_id IS 'String. Unique ID of the channel within telemetr.io';
          public          postgres    false    379            �           0    0 %   COLUMN telegram_channels.telemetr_url    COMMENT     m   COMMENT ON COLUMN public.telegram_channels.telemetr_url IS 'String. URL of the channel page on telemetr.io';
          public          postgres    false    379            �           0    0 !   COLUMN telegram_channels.relevant    COMMENT     �   COMMENT ON COLUMN public.telegram_channels.relevant IS 'Bool. Indicates if the channel should be displayed in the project web app';
          public          postgres    false    379            �           0    0 #   COLUMN telegram_channels.population    COMMENT     a   COMMENT ON COLUMN public.telegram_channels.population IS 'Int. Indicates number of subscribers';
          public          postgres    false    379            �           0    0 .   COLUMN telegram_channels.population_checked_on    COMMENT     �   COMMENT ON COLUMN public.telegram_channels.population_checked_on IS 'Date. Day when channel data was updated or when channel stats was updated';
          public          postgres    false    379            �           0    0    COLUMN telegram_channels.handle    COMMENT     [   COMMENT ON COLUMN public.telegram_channels.handle IS 'String. Unique Telegram identifier';
          public          postgres    false    379            �           0    0    COLUMN telegram_channels.status    COMMENT     f   COMMENT ON COLUMN public.telegram_channels.status IS 'Bool. False if the channel was deleted/banned';
          public          postgres    false    379            �           0    0 "   COLUMN telegram_channels.origin_id    COMMENT     f   COMMENT ON COLUMN public.telegram_channels.origin_id IS 'Int. Unique Telegram identifier (internal)';
          public          postgres    false    379            �           0    0 &   COLUMN telegram_channels.is_restricted    COMMENT     Z   COMMENT ON COLUMN public.telegram_channels.is_restricted IS 'Bool. Telegram system flag';
          public          postgres    false    379            �           0    0     COLUMN telegram_channels.is_fake    COMMENT     T   COMMENT ON COLUMN public.telegram_channels.is_fake IS 'Bool. Telegram system flag';
          public          postgres    false    379            �           0    0     COLUMN telegram_channels.is_scam    COMMENT     T   COMMENT ON COLUMN public.telegram_channels.is_scam IS 'Bool. Telegram system flag';
          public          postgres    false    379            �           0    0 #   COLUMN telegram_channels.no_forward    COMMENT     W   COMMENT ON COLUMN public.telegram_channels.no_forward IS 'Bool. Telegram system flag';
          public          postgres    false    379            �           0    0 %   COLUMN telegram_channels.restrictions    COMMENT     b   COMMENT ON COLUMN public.telegram_channels.restrictions IS 'List of JSON. Telegram system thing';
          public          postgres    false    379            �           0    0 '   COLUMN telegram_channels.linked_chat_id    COMMENT     �   COMMENT ON COLUMN public.telegram_channels.linked_chat_id IS 'Int. Telegram system thing. If present, the same as channel identifier';
          public          postgres    false    379            �           0    0    TABLE telegram_channels    ACL     :   GRANT ALL ON TABLE public.telegram_channels TO teledummy;
          public          postgres    false    379            |           1259    918241    telegram_channels_id_seq    SEQUENCE     �   ALTER TABLE public.telegram_channels ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.telegram_channels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    379            }           1259    918242 
   text_media    TABLE     f  CREATE TABLE public.text_media (
    id bigint NOT NULL,
    title text,
    url text,
    published timestamp with time zone,
    relevant boolean,
    excerpt text,
    content text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    author_data jsonb,
    first_img_data jsonb,
    source_id bigint NOT NULL,
    additional_data jsonb
);
    DROP TABLE public.text_media;
       public         heap    postgres    false    15            ~           1259    918248    text_media_id_seq    SEQUENCE     �   ALTER TABLE public.text_media ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.text_media_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    381                       1259    918249    theory    TABLE     @  CREATE TABLE public.theory (
    id bigint NOT NULL,
    title jsonb,
    type text,
    excerpt jsonb,
    images text[],
    content jsonb,
    original_content_metadata jsonb[],
    added_at timestamp with time zone DEFAULT now(),
    publish_date timestamp with time zone,
    updated_on timestamp with time zone
);
    DROP TABLE public.theory;
       public         heap    postgres    false    15            �           1259    918255    theory_id_seq    SEQUENCE     �   ALTER TABLE public.theory ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.theory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    383            �           1259    918256    websites    TABLE     �   CREATE TABLE public.websites (
    id bigint NOT NULL,
    url text NOT NULL,
    alive boolean DEFAULT true,
    api_url text,
    included boolean DEFAULT false NOT NULL,
    item_selector text,
    categories text[],
    cats_suffix text
);
    DROP TABLE public.websites;
       public         heap    postgres    false    15            �           1259    918263    websites_id_seq    SEQUENCE     �   ALTER TABLE public.websites ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.websites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    385            �           1259    918264    youtube_authors    TABLE     n   CREATE TABLE public.youtube_authors (
    id bigint NOT NULL,
    channel_id bigint,
    person_id integer
);
 #   DROP TABLE public.youtube_authors;
       public         heap    postgres    false    15            �           1259    918267    youtube_authors_id_seq    SEQUENCE     �   ALTER TABLE public.youtube_authors ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.youtube_authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    387    15            �           1259    918268    youtube_channels    TABLE     a  CREATE TABLE public.youtube_channels (
    id bigint NOT NULL,
    title text,
    youtube_id text,
    date_created timestamp without time zone,
    description text,
    subs_count bigint,
    vids_count bigint,
    views_count bigint,
    uploads_playlist_id text,
    stats_updated_on timestamp without time zone,
    status boolean DEFAULT true
);
 $   DROP TABLE public.youtube_channels;
       public         heap    postgres    false    15            �           0    0    TABLE youtube_channels    COMMENT     U   COMMENT ON TABLE public.youtube_channels IS 'Relevant channels on Youtube platform';
          public          postgres    false    389            �           0    0 "   COLUMN youtube_channels.youtube_id    COMMENT     ]   COMMENT ON COLUMN public.youtube_channels.youtube_id IS 'String. Unique YouTube identifier';
          public          postgres    false    389            �           0    0 "   COLUMN youtube_channels.subs_count    COMMENT     V   COMMENT ON COLUMN public.youtube_channels.subs_count IS 'Int. Number of subscribers';
          public          postgres    false    389            �           0    0 "   COLUMN youtube_channels.vids_count    COMMENT     [   COMMENT ON COLUMN public.youtube_channels.vids_count IS 'Int. Number of published videos';
          public          postgres    false    389            �           0    0 #   COLUMN youtube_channels.views_count    COMMENT     Y   COMMENT ON COLUMN public.youtube_channels.views_count IS 'Int. Overall number of views';
          public          postgres    false    389            �           0    0 +   COLUMN youtube_channels.uploads_playlist_id    COMMENT     q   COMMENT ON COLUMN public.youtube_channels.uploads_playlist_id IS 'String. Unique YouTube identifier (internal)';
          public          postgres    false    389            �           0    0    COLUMN youtube_channels.status    COMMENT     m   COMMENT ON COLUMN public.youtube_channels.status IS 'Bool. False if the channel has been removed or banned';
          public          postgres    false    389            �           1259    918274    youtube_channels_id_seq    SEQUENCE     �   ALTER TABLE public.youtube_channels ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.youtube_channels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    15    389            �           1259    918275    youtube_vids    TABLE     �  CREATE TABLE public.youtube_vids (
    title text,
    id integer NOT NULL,
    youtube_id text,
    segment_id integer,
    duration bigint,
    description text,
    youtube_stats jsonb,
    youtube_stats_updated_on date,
    youtube_channel_id bigint NOT NULL,
    timestamp_aired timestamp without time zone,
    url_is_alive boolean DEFAULT true NOT NULL,
    have boolean DEFAULT false NOT NULL,
    need boolean,
    private boolean DEFAULT false NOT NULL
);
     DROP TABLE public.youtube_vids;
       public         heap    postgres    false    15            �           0    0    TABLE youtube_vids    COMMENT     N   COMMENT ON TABLE public.youtube_vids IS 'Episodes from the Youtube platform';
          public          postgres    false    391            �           0    0    COLUMN youtube_vids.youtube_id    COMMENT     Y   COMMENT ON COLUMN public.youtube_vids.youtube_id IS 'String. Unique YouTube identifier';
          public          postgres    false    391            �           0    0    COLUMN youtube_vids.duration    COMMENT     ]   COMMENT ON COLUMN public.youtube_vids.duration IS 'Int. Duration of the episode in seconds';
          public          postgres    false    391            �           0    0 !   COLUMN youtube_vids.youtube_stats    COMMENT     �   COMMENT ON COLUMN public.youtube_vids.youtube_stats IS 'JSONB. YouTube statistics, with keys such as views and likes, and integers for values';
          public          postgres    false    391            �           0    0     COLUMN youtube_vids.url_is_alive    COMMENT     w   COMMENT ON COLUMN public.youtube_vids.url_is_alive IS 'Bool. Indicates if the URL worked when download was attempted';
          public          postgres    false    391            �           0    0    COLUMN youtube_vids.have    COMMENT     p   COMMENT ON COLUMN public.youtube_vids.have IS 'Bool. Indicate if video or audio of the episode was downloaded';
          public          postgres    false    391            �           1259    918283    youtube_vids_id_seq    SEQUENCE     �   ALTER TABLE public.youtube_vids ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.youtube_vids_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    391    15            �           2606    1833468    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            postgres    false    301            �           2606    1833473 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            postgres    false    303    303            �           2606    1833475 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            postgres    false    303            �           2606    1833470    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            postgres    false    301            �           2606    1833479 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            postgres    false    305    305            �           2606    1833481 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            postgres    false    305            �           2606    1833489 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public            postgres    false    308            �           2606    1833491 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public            postgres    false    308    308            �           2606    1833484    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public            postgres    false    307            �           2606    1833495 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public            postgres    false    311            �           2606    1833497 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public            postgres    false    311    311            �           2606    1833486     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public            postgres    false    307            �           2606    1833506    days_of_war days_of_war_day_key 
   CONSTRAINT     ^   ALTER TABLE ONLY public.days_of_war
    ADD CONSTRAINT days_of_war_day_key UNIQUE (day_date);
 I   ALTER TABLE ONLY public.days_of_war DROP CONSTRAINT days_of_war_day_key;
       public            postgres    false    313            �           2606    1833508    days_of_war days_of_war_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.days_of_war
    ADD CONSTRAINT days_of_war_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.days_of_war DROP CONSTRAINT days_of_war_pkey;
       public            postgres    false    313            �           2606    1833510 +   dentv_episodes dentv_episodes_dentv_url_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.dentv_episodes
    ADD CONSTRAINT dentv_episodes_dentv_url_key UNIQUE (dentv_url);
 U   ALTER TABLE ONLY public.dentv_episodes DROP CONSTRAINT dentv_episodes_dentv_url_key;
       public            postgres    false    315            �           2606    1833512 ,   dentv_episodes dentv_episodes_direct_url_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.dentv_episodes
    ADD CONSTRAINT dentv_episodes_direct_url_key UNIQUE (direct_url);
 V   ALTER TABLE ONLY public.dentv_episodes DROP CONSTRAINT dentv_episodes_direct_url_key;
       public            postgres    false    315            �           2606    1833514 "   dentv_episodes dentv_episodes_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.dentv_episodes
    ADD CONSTRAINT dentv_episodes_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.dentv_episodes DROP CONSTRAINT dentv_episodes_pkey;
       public            postgres    false    315            �           2606    1833517 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            postgres    false    317            �           2606    1833521 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            postgres    false    319    319            �           2606    1833523 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            postgres    false    319            �           2606    1833525 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            postgres    false    321            �           2606    1833555 ,   komso_episodes komso_episodes_direct_url_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.komso_episodes
    ADD CONSTRAINT komso_episodes_direct_url_key UNIQUE (direct_url);
 V   ALTER TABLE ONLY public.komso_episodes DROP CONSTRAINT komso_episodes_direct_url_key;
       public            postgres    false    323            �           2606    1833560 *   komso_episodes komso_episodes_komso_id_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.komso_episodes
    ADD CONSTRAINT komso_episodes_komso_id_key UNIQUE (komso_id);
 T   ALTER TABLE ONLY public.komso_episodes DROP CONSTRAINT komso_episodes_komso_id_key;
       public            postgres    false    323            �           2606    1833562 +   komso_episodes komso_episodes_komso_url_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.komso_episodes
    ADD CONSTRAINT komso_episodes_komso_url_key UNIQUE (komso_url);
 U   ALTER TABLE ONLY public.komso_episodes DROP CONSTRAINT komso_episodes_komso_url_key;
       public            postgres    false    323            �           2606    1833564 "   komso_episodes komso_episodes_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.komso_episodes
    ADD CONSTRAINT komso_episodes_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.komso_episodes DROP CONSTRAINT komso_episodes_pkey;
       public            postgres    false    323            �           2606    1833574 *   media_segments media_segments_komso_id_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT media_segments_komso_id_key UNIQUE (komso_id);
 T   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT media_segments_komso_id_key;
       public            postgres    false    328            �           2606    1833576 (   media_segments media_segments_ntv_id_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT media_segments_ntv_id_key UNIQUE (ntv_id);
 R   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT media_segments_ntv_id_key;
       public            postgres    false    328            �           2606    1833578 +   media_segments media_segments_rutube_id_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT media_segments_rutube_id_key UNIQUE (rutube_id);
 U   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT media_segments_rutube_id_key;
       public            postgres    false    328            �           2606    1833580 ,   media_segments media_segments_smotrim_id_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT media_segments_smotrim_id_key UNIQUE (smotrim_id);
 V   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT media_segments_smotrim_id_key;
       public            postgres    false    328            �           2606    1833610 B   msegments_to_rchannels_mapping msegments_to_rchannels_mapping_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.msegments_to_rchannels_mapping
    ADD CONSTRAINT msegments_to_rchannels_mapping_pkey PRIMARY KEY (id);
 l   ALTER TABLE ONLY public.msegments_to_rchannels_mapping DROP CONSTRAINT msegments_to_rchannels_mapping_pkey;
       public            postgres    false    330            �           2606    1833612 B   msegments_to_ychannels_mapping msegments_to_ychannels_mapping_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.msegments_to_ychannels_mapping
    ADD CONSTRAINT msegments_to_ychannels_mapping_pkey PRIMARY KEY (id);
 l   ALTER TABLE ONLY public.msegments_to_ychannels_mapping DROP CONSTRAINT msegments_to_ychannels_mapping_pkey;
       public            postgres    false    332            �           2606    1833614    ntv_episodes ntv_episodes_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.ntv_episodes
    ADD CONSTRAINT ntv_episodes_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.ntv_episodes DROP CONSTRAINT ntv_episodes_pkey;
       public            postgres    false    334            �           2606    1833616 '   ntv_episodes ntv_episodes_rutube_id_key 
   CONSTRAINT     g   ALTER TABLE ONLY public.ntv_episodes
    ADD CONSTRAINT ntv_episodes_rutube_id_key UNIQUE (rutube_id);
 Q   ALTER TABLE ONLY public.ntv_episodes DROP CONSTRAINT ntv_episodes_rutube_id_key;
       public            postgres    false    334            �           2606    1833618 !   ntv_episodes ntv_episodes_url_key 
   CONSTRAINT     ^   ALTER TABLE ONLY public.ntv_episodes
    ADD CONSTRAINT ntv_episodes_url_key UNIQUE (ntv_id);
 K   ALTER TABLE ONLY public.ntv_episodes DROP CONSTRAINT ntv_episodes_url_key;
       public            postgres    false    334            �           2606    1833566 3   media_coverage_type organization_coverage_type_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public.media_coverage_type
    ADD CONSTRAINT organization_coverage_type_pkey PRIMARY KEY (id);
 ]   ALTER TABLE ONLY public.media_coverage_type DROP CONSTRAINT organization_coverage_type_pkey;
       public            postgres    false    326            �           2606    1833568 <   media_coverage_type organization_coverage_type_type_name_key 
   CONSTRAINT     |   ALTER TABLE ONLY public.media_coverage_type
    ADD CONSTRAINT organization_coverage_type_type_name_key UNIQUE (type_name);
 f   ALTER TABLE ONLY public.media_coverage_type DROP CONSTRAINT organization_coverage_type_type_name_key;
       public            postgres    false    326            �           2606    1833624 6   organization_type organization_media_type_org_type_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.organization_type
    ADD CONSTRAINT organization_media_type_org_type_key UNIQUE (org_type);
 `   ALTER TABLE ONLY public.organization_type DROP CONSTRAINT organization_media_type_org_type_key;
       public            postgres    false    337            �           2606    1833626 .   organization_type organization_media_type_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.organization_type
    ADD CONSTRAINT organization_media_type_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.organization_type DROP CONSTRAINT organization_media_type_pkey;
       public            postgres    false    337            �           2606    1833628 "   organizations organizations_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_id_key UNIQUE (id);
 L   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_id_key;
       public            postgres    false    339            �           2606    1833630     organizations organizations_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_pkey;
       public            postgres    false    339            �           2606    1833632 *   organizations organizations_source_url_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_source_url_key UNIQUE (source_url);
 T   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_source_url_key;
       public            postgres    false    339            �           2606    1833642 8   people_3rdprt_details_raw people_3rdprt_details_raw_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.people_3rdprt_details_raw
    ADD CONSTRAINT people_3rdprt_details_raw_pkey PRIMARY KEY (person_id, url);
 b   ALTER TABLE ONLY public.people_3rdprt_details_raw DROP CONSTRAINT people_3rdprt_details_raw_pkey;
       public            postgres    false    344    344            �           2606    1833644 "   people_bundles people_bundles_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.people_bundles
    ADD CONSTRAINT people_bundles_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.people_bundles DROP CONSTRAINT people_bundles_pkey;
       public            postgres    false    346            �           2606    1833646 (   people_in_bundles people_in_bundles_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.people_in_bundles
    ADD CONSTRAINT people_in_bundles_pkey PRIMARY KEY (person_id, bundle_id);
 R   ALTER TABLE ONLY public.people_in_bundles DROP CONSTRAINT people_in_bundles_pkey;
       public            postgres    false    348    348            �           2606    1833648 $   people_in_orgs people_in_orgs_id_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.people_in_orgs
    ADD CONSTRAINT people_in_orgs_id_key UNIQUE (id);
 N   ALTER TABLE ONLY public.people_in_orgs DROP CONSTRAINT people_in_orgs_id_key;
       public            postgres    false    342            �           2606    1833650 "   people_in_orgs people_in_orgs_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.people_in_orgs
    ADD CONSTRAINT people_in_orgs_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.people_in_orgs DROP CONSTRAINT people_in_orgs_pkey;
       public            postgres    false    342            �           2606    1833652    people_in_ur people_in_ur_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.people_in_ur
    ADD CONSTRAINT people_in_ur_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.people_in_ur DROP CONSTRAINT people_in_ur_pkey;
       public            postgres    false    351            �           2606    1833654 !   people_in_ur people_in_ur_url_key 
   CONSTRAINT     [   ALTER TABLE ONLY public.people_in_ur
    ADD CONSTRAINT people_in_ur_url_key UNIQUE (url);
 K   ALTER TABLE ONLY public.people_in_ur DROP CONSTRAINT people_in_ur_url_key;
       public            postgres    false    351            �           2606    1833656 &   people_on_photos people_on_photos_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY public.people_on_photos
    ADD CONSTRAINT people_on_photos_pkey PRIMARY KEY (person_id, photo_id);
 P   ALTER TABLE ONLY public.people_on_photos DROP CONSTRAINT people_on_photos_pkey;
       public            postgres    false    353    353            �           2606    1833658 *   people_on_smotrim people_on_smotrim_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.people_on_smotrim
    ADD CONSTRAINT people_on_smotrim_id_key UNIQUE (id);
 T   ALTER TABLE ONLY public.people_on_smotrim DROP CONSTRAINT people_on_smotrim_id_key;
       public            postgres    false    355                        2606    1833660 (   people_on_smotrim people_on_smotrim_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.people_on_smotrim
    ADD CONSTRAINT people_on_smotrim_pkey PRIMARY KEY (person_id, episode_id, media_role_id);
 R   ALTER TABLE ONLY public.people_on_smotrim DROP CONSTRAINT people_on_smotrim_pkey;
       public            postgres    false    355    355    355                       2606    1833662 (   people_on_youtube people_on_youtube_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.people_on_youtube
    ADD CONSTRAINT people_on_youtube_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.people_on_youtube DROP CONSTRAINT people_on_youtube_pkey;
       public            postgres    false    357                       2606    1833664 <   people_to_msegments_mapping people_to_msegments_mapping_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY public.people_to_msegments_mapping
    ADD CONSTRAINT people_to_msegments_mapping_pkey PRIMARY KEY (id);
 f   ALTER TABLE ONLY public.people_to_msegments_mapping DROP CONSTRAINT people_to_msegments_mapping_pkey;
       public            postgres    false    359            �           2606    1833638    people person_fullname_key 
   CONSTRAINT     j   ALTER TABLE ONLY public.people
    ADD CONSTRAINT person_fullname_key UNIQUE (fullname_en, namesake_seq);
 D   ALTER TABLE ONLY public.people DROP CONSTRAINT person_fullname_key;
       public            postgres    false    341    341            �           2606    1833570 "   media_roles person_media_role_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.media_roles
    ADD CONSTRAINT person_media_role_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.media_roles DROP CONSTRAINT person_media_role_pkey;
       public            postgres    false    327            �           2606    1833572 &   media_roles person_media_role_role_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.media_roles
    ADD CONSTRAINT person_media_role_role_key UNIQUE (role);
 P   ALTER TABLE ONLY public.media_roles DROP CONSTRAINT person_media_role_role_key;
       public            postgres    false    327            �           2606    1833640    people person_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.people
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.people DROP CONSTRAINT person_pkey;
       public            postgres    false    341                       2606    1833666    photos photos_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.photos DROP CONSTRAINT photos_pkey;
       public            postgres    false    363                       2606    1833670    printed printed_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.printed
    ADD CONSTRAINT printed_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.printed DROP CONSTRAINT printed_pkey;
       public            postgres    false    365            
           2606    1833672    printed printed_storage_ref_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.printed
    ADD CONSTRAINT printed_storage_ref_key UNIQUE (storage_ref);
 I   ALTER TABLE ONLY public.printed DROP CONSTRAINT printed_storage_ref_key;
       public            postgres    false    365                       2606    1833678 8   printed_to_people_mapping printed_to_people_mapping_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.printed_to_people_mapping
    ADD CONSTRAINT printed_to_people_mapping_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.printed_to_people_mapping DROP CONSTRAINT printed_to_people_mapping_pkey;
       public            postgres    false    367                       2606    1833680    quotes quotes_id_key 
   CONSTRAINT     M   ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_id_key UNIQUE (id);
 >   ALTER TABLE ONLY public.quotes DROP CONSTRAINT quotes_id_key;
       public            postgres    false    369                       2606    1833682    quotes quotes_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.quotes DROP CONSTRAINT quotes_pkey;
       public            postgres    false    369                       2606    1833708 $   rutube_channels rutube_channels_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.rutube_channels
    ADD CONSTRAINT rutube_channels_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.rutube_channels DROP CONSTRAINT rutube_channels_pkey;
       public            postgres    false    371                       2606    1833710 5   rutube_channels rutube_channels_rutube_channel_id_key 
   CONSTRAINT     }   ALTER TABLE ONLY public.rutube_channels
    ADD CONSTRAINT rutube_channels_rutube_channel_id_key UNIQUE (rutube_channel_id);
 _   ALTER TABLE ONLY public.rutube_channels DROP CONSTRAINT rutube_channels_rutube_channel_id_key;
       public            postgres    false    371                       2606    1833712    rutube_vids rutube_vids_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.rutube_vids
    ADD CONSTRAINT rutube_vids_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.rutube_vids DROP CONSTRAINT rutube_vids_pkey;
       public            postgres    false    373                       2606    1833739 &   smotrim_episodes smotrim_episodes_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.smotrim_episodes
    ADD CONSTRAINT smotrim_episodes_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.smotrim_episodes DROP CONSTRAINT smotrim_episodes_pkey;
       public            postgres    false    375                       2606    1833741 0   smotrim_episodes smotrim_episodes_smotrim_id_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.smotrim_episodes
    ADD CONSTRAINT smotrim_episodes_smotrim_id_key UNIQUE (smotrim_id);
 Z   ALTER TABLE ONLY public.smotrim_episodes DROP CONSTRAINT smotrim_episodes_smotrim_id_key;
       public            postgres    false    375            �           2606    1833582 0   media_segments solovyovlive_segment_types_id_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT solovyovlive_segment_types_id_key UNIQUE (id);
 Z   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT solovyovlive_segment_types_id_key;
       public            postgres    false    328            �           2606    1833584 .   media_segments solovyovlive_segment_types_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT solovyovlive_segment_types_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT solovyovlive_segment_types_pkey;
       public            postgres    false    328                       2606    1833762 &   telegram_authors telegram_authors_pkey 
   CONSTRAINT     w   ALTER TABLE ONLY public.telegram_authors
    ADD CONSTRAINT telegram_authors_pkey PRIMARY KEY (person_id, channel_id);
 P   ALTER TABLE ONLY public.telegram_authors DROP CONSTRAINT telegram_authors_pkey;
       public            postgres    false    377    377                       2606    1833764 .   telegram_channels telegram_channels_handle_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.telegram_channels
    ADD CONSTRAINT telegram_channels_handle_key UNIQUE (handle);
 X   ALTER TABLE ONLY public.telegram_channels DROP CONSTRAINT telegram_channels_handle_key;
       public            postgres    false    379                        2606    1833766 (   telegram_channels telegram_channels_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.telegram_channels
    ADD CONSTRAINT telegram_channels_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.telegram_channels DROP CONSTRAINT telegram_channels_pkey;
       public            postgres    false    379            "           2606    1833768 3   telegram_channels telegram_channels_telemetr_id_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.telegram_channels
    ADD CONSTRAINT telegram_channels_telemetr_id_key UNIQUE (telemetr_id);
 ]   ALTER TABLE ONLY public.telegram_channels DROP CONSTRAINT telegram_channels_telemetr_id_key;
       public            postgres    false    379            $           2606    1833776    text_media text_media_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.text_media
    ADD CONSTRAINT text_media_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.text_media DROP CONSTRAINT text_media_pkey;
       public            postgres    false    381            &           2606    1833778    text_media text_media_url_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.text_media
    ADD CONSTRAINT text_media_url_key UNIQUE (url);
 G   ALTER TABLE ONLY public.text_media DROP CONSTRAINT text_media_url_key;
       public            postgres    false    381            (           2606    1833780    theory theory_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.theory
    ADD CONSTRAINT theory_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.theory DROP CONSTRAINT theory_pkey;
       public            postgres    false    383            *           2606    1833827    websites websites_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.websites
    ADD CONSTRAINT websites_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.websites DROP CONSTRAINT websites_pkey;
       public            postgres    false    385            ,           2606    1833829    websites websites_url_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.websites
    ADD CONSTRAINT websites_url_key UNIQUE (url);
 C   ALTER TABLE ONLY public.websites DROP CONSTRAINT websites_url_key;
       public            postgres    false    385            .           2606    1833831 $   youtube_authors youtube_authors_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.youtube_authors
    ADD CONSTRAINT youtube_authors_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.youtube_authors DROP CONSTRAINT youtube_authors_pkey;
       public            postgres    false    387            0           2606    1833833 &   youtube_channels youtube_channels_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.youtube_channels
    ADD CONSTRAINT youtube_channels_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.youtube_channels DROP CONSTRAINT youtube_channels_pkey;
       public            postgres    false    389            2           2606    1833835 0   youtube_channels youtube_channels_youtube_id_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.youtube_channels
    ADD CONSTRAINT youtube_channels_youtube_id_key UNIQUE (youtube_id);
 Z   ALTER TABLE ONLY public.youtube_channels DROP CONSTRAINT youtube_channels_youtube_id_key;
       public            postgres    false    389            4           2606    1833837    youtube_vids youtube_vids_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.youtube_vids
    ADD CONSTRAINT youtube_vids_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.youtube_vids DROP CONSTRAINT youtube_vids_pkey;
       public            postgres    false    391            6           2606    1833839 (   youtube_vids youtube_vids_youtube_id_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.youtube_vids
    ADD CONSTRAINT youtube_vids_youtube_id_key UNIQUE (youtube_id);
 R   ALTER TABLE ONLY public.youtube_vids DROP CONSTRAINT youtube_vids_youtube_id_key;
       public            postgres    false    391            �           1259    1833471    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            postgres    false    301            �           1259    1833476 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            postgres    false    303            �           1259    1833477 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            postgres    false    303            �           1259    1833482 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            postgres    false    305            �           1259    1833492 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public            postgres    false    308            �           1259    1833493 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public            postgres    false    308            �           1259    1833498 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public            postgres    false    311            �           1259    1833499 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public            postgres    false    311            �           1259    1833487     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public            postgres    false    307            �           1259    1833518 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            postgres    false    317            �           1259    1833519 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            postgres    false    317            
           2618    1834348    msegments_extended _RETURN    RULE     �  CREATE OR REPLACE VIEW public.msegments_extended AS
 SELECT ms.name_ru,
    ms.name_en,
    ms.name_uk,
    ms.cluster,
    ms.segment_type,
    ms.latest_episode_date,
    o.name_ru AS parent_org,
    mss.total,
    mss.total_time,
    mss.transcribed,
    mss.transcribed_time,
    mss.have,
    mss.have_time
   FROM ((public.media_segments ms
     LEFT JOIN service.media_segments_stats mss ON ((ms.id = mss.segment_id)))
     LEFT JOIN public.organizations o ON ((ms.parent_org_id = o.id)))
  WHERE ((ms.relevant IS TRUE) AND (ms.is_defunct IS NOT TRUE) AND (mss.day_date = ( SELECT max(media_segments_stats.day_date) AS max
           FROM service.media_segments_stats
          WHERE (media_segments_stats.segment_id = ms.id))))
  GROUP BY ms.cluster, o.name_ru, ms.id, mss.total, mss.total_time, mss.transcribed, mss.transcribed_time, mss.have, mss.have_time
  ORDER BY ms.cluster, ms.name_ru;
 �  CREATE OR REPLACE VIEW public.msegments_extended AS
SELECT
    NULL::text AS name_ru,
    NULL::text AS name_en,
    NULL::text AS name_uk,
    NULL::text AS cluster,
    NULL::text AS segment_type,
    NULL::timestamp with time zone AS latest_episode_date,
    NULL::text AS parent_org,
    NULL::integer AS total,
    NULL::double precision AS total_time,
    NULL::integer AS transcribed,
    NULL::double precision AS transcribed_time,
    NULL::integer AS have,
    NULL::double precision AS have_time;
       public          postgres    false    328    328    328    328    4308    328    328    328    328    328    328    339    339    403                       2618    2582507    people_extended _RETURN    RULE     �  CREATE OR REPLACE VIEW public.people_extended AS
 SELECT p.id,
    p.fullname_uk,
    p.fullname_ru,
    p.fullname_en,
    p.lastname_en,
    p.lastname_ru,
    p.social,
    p.dob,
    p.contact,
    p.address,
    p.associates,
    p.additional,
    p.aliases,
    p.info,
    p.dod,
    p.cod,
    p.known_for,
    p.wiki_ref,
    COALESCE(public.get_person_photo(p.id, 'large'::text), public.get_default_photo('large'::text, p.sex)) AS photo,
    public.get_person_external_links(p.id) AS external_links,
    public.get_person_bundles(p.id) AS bundles,
    COALESCE(public.get_person_photo(p.id, 'thumb'::text), public.get_default_photo('thumb'::text, p.sex)) AS thumb,
    p.added_on,
    public.get_orgs_data(public.get_patient_orgs_idx((p.id)::bigint)) AS orgs,
    p.sex,
    public.get_tchannels_data(public.get_patient_tchannels_idx((p.id)::bigint)) AS telegram_channels,
    public.get_ychannels_data(public.get_patient_ychannels_idx((p.id)::bigint)) AS youtube_channels
   FROM ((public.people p
     LEFT JOIN public.people_on_photos pop ON ((p.id = pop.person_id)))
     LEFT JOIN public.photos ph ON ((pop.photo_id = ph.id)))
  WHERE (p.relevant IS TRUE)
  GROUP BY p.id
  ORDER BY p.lastname_ru;
 j  CREATE OR REPLACE VIEW public.people_extended AS
SELECT
    NULL::integer AS id,
    NULL::text AS fullname_uk,
    NULL::text AS fullname_ru,
    NULL::text AS fullname_en,
    NULL::text AS lastname_en,
    NULL::text AS lastname_ru,
    NULL::text[] AS social,
    NULL::date AS dob,
    NULL::jsonb AS contact,
    NULL::text[] AS address,
    NULL::jsonb[] AS associates,
    NULL::jsonb AS additional,
    NULL::jsonb[] AS aliases,
    NULL::jsonb AS info,
    NULL::date AS dod,
    NULL::character varying AS cod,
    NULL::jsonb AS known_for,
    NULL::jsonb AS wiki_ref,
    NULL::text AS photo,
    NULL::text[] AS external_links,
    NULL::jsonb[] AS bundles,
    NULL::text AS thumb,
    NULL::timestamp with time zone AS added_on,
    NULL::jsonb[] AS orgs,
    NULL::text AS sex,
    NULL::jsonb[] AS telegram_channels,
    NULL::jsonb[] AS youtube_channels;
       public          postgres    false    520    341    341    341    341    341    341    341    341    341    341    341    341    341    341    341    341    353    353    363    4332    341    341    341    341    341    561    556    543    542    541    540    539    538    536    410            r           2620    918742    media_segments msegments_upup    TRIGGER        CREATE TRIGGER msegments_upup BEFORE UPDATE ON public.media_segments FOR EACH ROW EXECUTE FUNCTION public.update_updated_on();
 6   DROP TRIGGER msegments_upup ON public.media_segments;
       public          postgres    false    328    597            s           2620    918743    organizations orgs_upup    TRIGGER     y   CREATE TRIGGER orgs_upup BEFORE UPDATE ON public.organizations FOR EACH ROW EXECUTE FUNCTION public.update_updated_on();
 0   DROP TRIGGER orgs_upup ON public.organizations;
       public          postgres    false    597    339            t           2620    918744    people people_upup    TRIGGER     t   CREATE TRIGGER people_upup BEFORE UPDATE ON public.people FOR EACH ROW EXECUTE FUNCTION public.update_updated_on();
 +   DROP TRIGGER people_upup ON public.people;
       public          postgres    false    341    597            u           2620    918745    theory theory_upup    TRIGGER     t   CREATE TRIGGER theory_upup BEFORE UPDATE ON public.theory FOR EACH ROW EXECUTE FUNCTION public.update_updated_on();
 +   DROP TRIGGER theory_upup ON public.theory;
       public          postgres    false    597    383            v           2620    918746 !   theory update_theory_date_trigger    TRIGGER     �   CREATE TRIGGER update_theory_date_trigger BEFORE INSERT OR UPDATE ON public.theory FOR EACH ROW EXECUTE FUNCTION public.update_date_published();
 :   DROP TRIGGER update_theory_date_trigger ON public.theory;
       public          postgres    false    383    589            7           2606    1833840 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          postgres    false    305    303    4243            8           2606    1833845 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          postgres    false    303    4232    301            9           2606    1833850 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          postgres    false    305    4278    319            :           2606    1833855 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public          postgres    false    4232    308    301            ;           2606    1833860 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public          postgres    false    4245    308    307            <           2606    1833865 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public          postgres    false    311    305    4243            =           2606    1833870 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public          postgres    false    4245    307    311            >           2606    1833875 -   dentv_episodes dentv_episodes_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dentv_episodes
    ADD CONSTRAINT dentv_episodes_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES public.media_segments(id);
 W   ALTER TABLE ONLY public.dentv_episodes DROP CONSTRAINT dentv_episodes_segment_id_fkey;
       public          postgres    false    328    4306    315            ?           2606    1833880 1   dentv_episodes dentv_episodes_youtube_rec_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dentv_episodes
    ADD CONSTRAINT dentv_episodes_youtube_rec_id_fkey FOREIGN KEY (youtube_rec_id) REFERENCES public.youtube_vids(id);
 [   ALTER TABLE ONLY public.dentv_episodes DROP CONSTRAINT dentv_episodes_youtube_rec_id_fkey;
       public          postgres    false    4404    315    391            @           2606    1833885 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          postgres    false    4278    317    319            A           2606    1833890 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public          postgres    false    4245    307    317            B           2606    1833935 -   komso_episodes komso_episodes_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.komso_episodes
    ADD CONSTRAINT komso_episodes_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES public.media_segments(id);
 W   ALTER TABLE ONLY public.komso_episodes DROP CONSTRAINT komso_episodes_segment_id_fkey;
       public          postgres    false    328    323    4306            C           2606    1833940 0   media_segments media_segments_parent_org_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.media_segments
    ADD CONSTRAINT media_segments_parent_org_id_fkey FOREIGN KEY (parent_org_id) REFERENCES public.organizations(id);
 Z   ALTER TABLE ONLY public.media_segments DROP CONSTRAINT media_segments_parent_org_id_fkey;
       public          postgres    false    4324    339    328            D           2606    1833970 S   msegments_to_rchannels_mapping msegments_to_rchannels_mapping_media_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.msegments_to_rchannels_mapping
    ADD CONSTRAINT msegments_to_rchannels_mapping_media_segment_id_fkey FOREIGN KEY (media_segment_id) REFERENCES public.media_segments(id);
 }   ALTER TABLE ONLY public.msegments_to_rchannels_mapping DROP CONSTRAINT msegments_to_rchannels_mapping_media_segment_id_fkey;
       public          postgres    false    4306    328    330            E           2606    1833975 T   msegments_to_rchannels_mapping msegments_to_rchannels_mapping_rutube_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.msegments_to_rchannels_mapping
    ADD CONSTRAINT msegments_to_rchannels_mapping_rutube_channel_id_fkey FOREIGN KEY (rutube_channel_id) REFERENCES public.rutube_channels(id);
 ~   ALTER TABLE ONLY public.msegments_to_rchannels_mapping DROP CONSTRAINT msegments_to_rchannels_mapping_rutube_channel_id_fkey;
       public          postgres    false    371    330    4370            F           2606    1833980 S   msegments_to_ychannels_mapping msegments_to_ychannels_mapping_media_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.msegments_to_ychannels_mapping
    ADD CONSTRAINT msegments_to_ychannels_mapping_media_segment_id_fkey FOREIGN KEY (media_segment_id) REFERENCES public.media_segments(id);
 }   ALTER TABLE ONLY public.msegments_to_ychannels_mapping DROP CONSTRAINT msegments_to_ychannels_mapping_media_segment_id_fkey;
       public          postgres    false    328    332    4306            G           2606    1833985 U   msegments_to_ychannels_mapping msegments_to_ychannels_mapping_youtube_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.msegments_to_ychannels_mapping
    ADD CONSTRAINT msegments_to_ychannels_mapping_youtube_channel_id_fkey FOREIGN KEY (youtube_channel_id) REFERENCES public.youtube_channels(id);
    ALTER TABLE ONLY public.msegments_to_ychannels_mapping DROP CONSTRAINT msegments_to_ychannels_mapping_youtube_channel_id_fkey;
       public          postgres    false    4400    332    389            H           2606    1833990 )   ntv_episodes ntv_episodes_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.ntv_episodes
    ADD CONSTRAINT ntv_episodes_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES public.media_segments(id);
 S   ALTER TABLE ONLY public.ntv_episodes DROP CONSTRAINT ntv_episodes_segment_id_fkey;
       public          postgres    false    328    4306    334            I           2606    1834000 4   organization_type organization_type_parent_type_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.organization_type
    ADD CONSTRAINT organization_type_parent_type_fkey FOREIGN KEY (parent_type) REFERENCES public.organization_type(id);
 ^   ALTER TABLE ONLY public.organization_type DROP CONSTRAINT organization_type_parent_type_fkey;
       public          postgres    false    337    4322    337            J           2606    1834005 1   organizations organizations_coverage_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_coverage_type_id_fkey FOREIGN KEY (coverage_type_id) REFERENCES public.media_coverage_type(id);
 [   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_coverage_type_id_fkey;
       public          postgres    false    339    326    4290            K           2606    1834010 )   organizations organizations_org_type_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_org_type_fkey FOREIGN KEY (org_type) REFERENCES enums.orgs_taxonomy(id);
 S   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_org_type_fkey;
       public          postgres    false    339            L           2606    1834015 ,   organizations organizations_org_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_org_type_id_fkey FOREIGN KEY (org_type_id) REFERENCES public.organization_type(id);
 V   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_org_type_id_fkey;
       public          postgres    false    339    4322    337            M           2606    1834020 .   organizations organizations_parent_org_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_parent_org_id_fkey FOREIGN KEY (parent_org_id) REFERENCES public.organizations(id);
 X   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_parent_org_id_fkey;
       public          postgres    false    4324    339    339            N           2606    1834025 '   organizations organizations_region_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_region_fkey FOREIGN KEY (region) REFERENCES future.rf_territorial(id);
 Q   ALTER TABLE ONLY public.organizations DROP CONSTRAINT organizations_region_fkey;
       public          postgres    false    339            S           2606    1834040 B   people_3rdprt_details_raw people_3rdprt_details_raw_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_3rdprt_details_raw
    ADD CONSTRAINT people_3rdprt_details_raw_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 l   ALTER TABLE ONLY public.people_3rdprt_details_raw DROP CONSTRAINT people_3rdprt_details_raw_person_id_fkey;
       public          postgres    false    344    4332    341            T           2606    1834045 .   people_bundles people_bundles_bundle_type_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_bundles
    ADD CONSTRAINT people_bundles_bundle_type_fkey FOREIGN KEY (bundle_type) REFERENCES enums.bundle_types(id);
 X   ALTER TABLE ONLY public.people_bundles DROP CONSTRAINT people_bundles_bundle_type_fkey;
       public          postgres    false    346            U           2606    1834050 3   people_bundles people_bundles_parent_bundle_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_bundles
    ADD CONSTRAINT people_bundles_parent_bundle_id_fkey FOREIGN KEY (parent_bundle_id) REFERENCES public.people_bundles(id);
 ]   ALTER TABLE ONLY public.people_bundles DROP CONSTRAINT people_bundles_parent_bundle_id_fkey;
       public          postgres    false    4340    346    346            V           2606    1834055 2   people_in_bundles people_in_bundles_bundle_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_bundles
    ADD CONSTRAINT people_in_bundles_bundle_id_fkey FOREIGN KEY (bundle_id) REFERENCES public.people_bundles(id);
 \   ALTER TABLE ONLY public.people_in_bundles DROP CONSTRAINT people_in_bundles_bundle_id_fkey;
       public          postgres    false    4340    348    346            W           2606    1834060 2   people_in_bundles people_in_bundles_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_bundles
    ADD CONSTRAINT people_in_bundles_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 \   ALTER TABLE ONLY public.people_in_bundles DROP CONSTRAINT people_in_bundles_person_id_fkey;
       public          postgres    false    4332    348    341            O           2606    1834065 )   people_in_orgs people_in_orgs_org_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_orgs
    ADD CONSTRAINT people_in_orgs_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id);
 S   ALTER TABLE ONLY public.people_in_orgs DROP CONSTRAINT people_in_orgs_org_id_fkey;
       public          postgres    false    339    4324    342            P           2606    1834070 ,   people_in_orgs people_in_orgs_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_orgs
    ADD CONSTRAINT people_in_orgs_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 V   ALTER TABLE ONLY public.people_in_orgs DROP CONSTRAINT people_in_orgs_person_id_fkey;
       public          postgres    false    341    342    4332            Q           2606    1834075 0   people_in_orgs people_in_orgs_role_category_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_orgs
    ADD CONSTRAINT people_in_orgs_role_category_fkey FOREIGN KEY (role_category) REFERENCES enums.isco08_taxonomy(id);
 Z   ALTER TABLE ONLY public.people_in_orgs DROP CONSTRAINT people_in_orgs_role_category_fkey;
       public          postgres    false    342            R           2606    1834080 +   people_in_orgs people_in_orgs_role_ref_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_orgs
    ADD CONSTRAINT people_in_orgs_role_ref_fkey FOREIGN KEY (role_ref) REFERENCES enums.isco08_index(id);
 U   ALTER TABLE ONLY public.people_in_orgs DROP CONSTRAINT people_in_orgs_role_ref_fkey;
       public          postgres    false    342            X           2606    1834085 (   people_in_ur people_in_ur_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_in_ur
    ADD CONSTRAINT people_in_ur_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 R   ALTER TABLE ONLY public.people_in_ur DROP CONSTRAINT people_in_ur_person_id_fkey;
       public          postgres    false    4332    351    341            Y           2606    1834090 0   people_on_photos people_on_photos_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_photos
    ADD CONSTRAINT people_on_photos_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 Z   ALTER TABLE ONLY public.people_on_photos DROP CONSTRAINT people_on_photos_person_id_fkey;
       public          postgres    false    341    353    4332            Z           2606    1834095 /   people_on_photos people_on_photos_photo_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_photos
    ADD CONSTRAINT people_on_photos_photo_id_fkey FOREIGN KEY (photo_id) REFERENCES public.photos(id);
 Y   ALTER TABLE ONLY public.people_on_photos DROP CONSTRAINT people_on_photos_photo_id_fkey;
       public          postgres    false    4358    353    363            [           2606    1834100 3   people_on_smotrim people_on_smotrim_episode_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_smotrim
    ADD CONSTRAINT people_on_smotrim_episode_id_fkey FOREIGN KEY (episode_id) REFERENCES public.smotrim_episodes(id);
 ]   ALTER TABLE ONLY public.people_on_smotrim DROP CONSTRAINT people_on_smotrim_episode_id_fkey;
       public          postgres    false    375    4376    355            \           2606    1834105 6   people_on_smotrim people_on_smotrim_media_role_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_smotrim
    ADD CONSTRAINT people_on_smotrim_media_role_id_fkey FOREIGN KEY (media_role_id) REFERENCES public.media_roles(id);
 `   ALTER TABLE ONLY public.people_on_smotrim DROP CONSTRAINT people_on_smotrim_media_role_id_fkey;
       public          postgres    false    355    4294    327            ]           2606    1834110 2   people_on_smotrim people_on_smotrim_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_smotrim
    ADD CONSTRAINT people_on_smotrim_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 \   ALTER TABLE ONLY public.people_on_smotrim DROP CONSTRAINT people_on_smotrim_person_id_fkey;
       public          postgres    false    341    355    4332            ^           2606    1834115 3   people_on_youtube people_on_youtube_episode_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_youtube
    ADD CONSTRAINT people_on_youtube_episode_id_fkey FOREIGN KEY (episode_id) REFERENCES public.youtube_vids(id);
 ]   ALTER TABLE ONLY public.people_on_youtube DROP CONSTRAINT people_on_youtube_episode_id_fkey;
       public          postgres    false    4404    357    391            _           2606    1834120 6   people_on_youtube people_on_youtube_media_role_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_youtube
    ADD CONSTRAINT people_on_youtube_media_role_id_fkey FOREIGN KEY (media_role_id) REFERENCES public.media_roles(id);
 `   ALTER TABLE ONLY public.people_on_youtube DROP CONSTRAINT people_on_youtube_media_role_id_fkey;
       public          postgres    false    4294    357    327            `           2606    1834125 2   people_on_youtube people_on_youtube_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_on_youtube
    ADD CONSTRAINT people_on_youtube_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 \   ALTER TABLE ONLY public.people_on_youtube DROP CONSTRAINT people_on_youtube_person_id_fkey;
       public          postgres    false    4332    357    341            a           2606    1834130 M   people_to_msegments_mapping people_to_msegments_mapping_media_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_to_msegments_mapping
    ADD CONSTRAINT people_to_msegments_mapping_media_segment_id_fkey FOREIGN KEY (media_segment_id) REFERENCES public.media_segments(id);
 w   ALTER TABLE ONLY public.people_to_msegments_mapping DROP CONSTRAINT people_to_msegments_mapping_media_segment_id_fkey;
       public          postgres    false    328    359    4306            b           2606    1834135 F   people_to_msegments_mapping people_to_msegments_mapping_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.people_to_msegments_mapping
    ADD CONSTRAINT people_to_msegments_mapping_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 p   ALTER TABLE ONLY public.people_to_msegments_mapping DROP CONSTRAINT people_to_msegments_mapping_person_id_fkey;
       public          postgres    false    359    4332    341            c           2606    1834160 B   printed_to_people_mapping printed_to_people_mapping_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.printed_to_people_mapping
    ADD CONSTRAINT printed_to_people_mapping_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 l   ALTER TABLE ONLY public.printed_to_people_mapping DROP CONSTRAINT printed_to_people_mapping_person_id_fkey;
       public          postgres    false    4332    367    341            d           2606    1834165 C   printed_to_people_mapping printed_to_people_mapping_printed_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.printed_to_people_mapping
    ADD CONSTRAINT printed_to_people_mapping_printed_id_fkey FOREIGN KEY (printed_id) REFERENCES public.printed(id);
 m   ALTER TABLE ONLY public.printed_to_people_mapping DROP CONSTRAINT printed_to_people_mapping_printed_id_fkey;
       public          postgres    false    367    365    4360            e           2606    1834170 I   printed_to_people_mapping printed_to_people_mapping_printed_piece_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.printed_to_people_mapping
    ADD CONSTRAINT printed_to_people_mapping_printed_piece_id_fkey FOREIGN KEY (printed_piece_id) REFERENCES data.printed_content(id);
 s   ALTER TABLE ONLY public.printed_to_people_mapping DROP CONSTRAINT printed_to_people_mapping_printed_piece_id_fkey;
       public          postgres    false    367            f           2606    1834175    quotes quotes_person_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 F   ALTER TABLE ONLY public.quotes DROP CONSTRAINT quotes_person_id_fkey;
       public          postgres    false    4332    341    369            g           2606    1834180    quotes quotes_source_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.organizations(id);
 F   ALTER TABLE ONLY public.quotes DROP CONSTRAINT quotes_source_id_fkey;
       public          postgres    false    339    4324    369            h           2606    1834190 -   rutube_vids rutube_vids_media_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rutube_vids
    ADD CONSTRAINT rutube_vids_media_segment_id_fkey FOREIGN KEY (media_segment_id) REFERENCES public.media_segments(id);
 W   ALTER TABLE ONLY public.rutube_vids DROP CONSTRAINT rutube_vids_media_segment_id_fkey;
       public          postgres    false    4306    328    373            i           2606    1834195 .   rutube_vids rutube_vids_rutube_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rutube_vids
    ADD CONSTRAINT rutube_vids_rutube_channel_id_fkey FOREIGN KEY (rutube_channel_id) REFERENCES public.rutube_channels(id);
 X   ALTER TABLE ONLY public.rutube_vids DROP CONSTRAINT rutube_vids_rutube_channel_id_fkey;
       public          postgres    false    373    4370    371            j           2606    1834220 1   smotrim_episodes smotrim_episodes_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.smotrim_episodes
    ADD CONSTRAINT smotrim_episodes_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES public.media_segments(id);
 [   ALTER TABLE ONLY public.smotrim_episodes DROP CONSTRAINT smotrim_episodes_segment_id_fkey;
       public          postgres    false    328    375    4306            k           2606    1834235 1   telegram_authors telegram_authors_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.telegram_authors
    ADD CONSTRAINT telegram_authors_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.telegram_channels(id);
 [   ALTER TABLE ONLY public.telegram_authors DROP CONSTRAINT telegram_authors_channel_id_fkey;
       public          postgres    false    377    379    4384            l           2606    1834240 0   telegram_authors telegram_authors_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.telegram_authors
    ADD CONSTRAINT telegram_authors_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 Z   ALTER TABLE ONLY public.telegram_authors DROP CONSTRAINT telegram_authors_person_id_fkey;
       public          postgres    false    4332    377    341            m           2606    1834255 $   text_media text_media_source_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.text_media
    ADD CONSTRAINT text_media_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.websites(id);
 N   ALTER TABLE ONLY public.text_media DROP CONSTRAINT text_media_source_id_fkey;
       public          postgres    false    4394    381    385            n           2606    1834325 /   youtube_authors youtube_authors_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.youtube_authors
    ADD CONSTRAINT youtube_authors_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.youtube_channels(id);
 Y   ALTER TABLE ONLY public.youtube_authors DROP CONSTRAINT youtube_authors_channel_id_fkey;
       public          postgres    false    389    4400    387            o           2606    1834330 .   youtube_authors youtube_authors_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.youtube_authors
    ADD CONSTRAINT youtube_authors_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(id);
 X   ALTER TABLE ONLY public.youtube_authors DROP CONSTRAINT youtube_authors_person_id_fkey;
       public          postgres    false    387    4332    341            p           2606    1834335 )   youtube_vids youtube_vids_segment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.youtube_vids
    ADD CONSTRAINT youtube_vids_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES public.media_segments(id);
 S   ALTER TABLE ONLY public.youtube_vids DROP CONSTRAINT youtube_vids_segment_id_fkey;
       public          postgres    false    328    391    4306            q           2606    1834340 1   youtube_vids youtube_vids_youtube_channel_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.youtube_vids
    ADD CONSTRAINT youtube_vids_youtube_channel_id_fkey FOREIGN KEY (youtube_channel_id) REFERENCES public.youtube_channels(id);
 [   ALTER TABLE ONLY public.youtube_vids DROP CONSTRAINT youtube_vids_youtube_channel_id_fkey;
       public          postgres    false    391    4400    389                       0    917997 
   auth_group    ROW SECURITY     8   ALTER TABLE public.auth_group ENABLE ROW LEVEL SECURITY;          public          postgres    false    301                       0    918001    auth_group_permissions    ROW SECURITY     D   ALTER TABLE public.auth_group_permissions ENABLE ROW LEVEL SECURITY;          public          postgres    false    303                       0    918005    auth_permission    ROW SECURITY     =   ALTER TABLE public.auth_permission ENABLE ROW LEVEL SECURITY;          public          postgres    false    305                       0    918009 	   auth_user    ROW SECURITY     7   ALTER TABLE public.auth_user ENABLE ROW LEVEL SECURITY;          public          postgres    false    307                       0    918012    auth_user_groups    ROW SECURITY     >   ALTER TABLE public.auth_user_groups ENABLE ROW LEVEL SECURITY;          public          postgres    false    308                       0    918017    auth_user_user_permissions    ROW SECURITY     H   ALTER TABLE public.auth_user_user_permissions ENABLE ROW LEVEL SECURITY;          public          postgres    false    311                       3256    919267    dentv_episodes dentv_read    POLICY     K   CREATE POLICY dentv_read ON public.dentv_episodes FOR SELECT USING (true);
 1   DROP POLICY dentv_read ON public.dentv_episodes;
       public          postgres    false    315                       3256    919268    dentv_episodes dentv_warp    POLICY     H   CREATE POLICY dentv_warp ON public.dentv_episodes TO warp USING (true);
 1   DROP POLICY dentv_warp ON public.dentv_episodes;
       public          postgres    false    315                       0    918036    django_admin_log    ROW SECURITY     >   ALTER TABLE public.django_admin_log ENABLE ROW LEVEL SECURITY;          public          postgres    false    317                       0    918043    django_content_type    ROW SECURITY     A   ALTER TABLE public.django_content_type ENABLE ROW LEVEL SECURITY;          public          postgres    false    319                       0    918047    django_migrations    ROW SECURITY     ?   ALTER TABLE public.django_migrations ENABLE ROW LEVEL SECURITY;          public          postgres    false    321                       3256    919269 "   ntv_episodes ntv_episodes_all_view    POLICY     T   CREATE POLICY ntv_episodes_all_view ON public.ntv_episodes FOR SELECT USING (true);
 :   DROP POLICY ntv_episodes_all_view ON public.ntv_episodes;
       public          postgres    false    334                       3256    919270 <   people_3rdprt_details_raw people_3rdprt_details_raw_all_view    POLICY     n   CREATE POLICY people_3rdprt_details_raw_all_view ON public.people_3rdprt_details_raw FOR SELECT USING (true);
 T   DROP POLICY people_3rdprt_details_raw_all_view ON public.people_3rdprt_details_raw;
       public          postgres    false    344                        3256    919271 ,   people_in_bundles people_in_bundles_all_view    POLICY     ^   CREATE POLICY people_in_bundles_all_view ON public.people_in_bundles FOR SELECT USING (true);
 D   DROP POLICY people_in_bundles_all_view ON public.people_in_bundles;
       public          postgres    false    348                       3256    919272 &   people_in_orgs people_in_orgs_all_view    POLICY     X   CREATE POLICY people_in_orgs_all_view ON public.people_in_orgs FOR SELECT USING (true);
 >   DROP POLICY people_in_orgs_all_view ON public.people_in_orgs;
       public          postgres    false    342            !           3256    919273 *   people_on_photos people_on_photos_all_view    POLICY     \   CREATE POLICY people_on_photos_all_view ON public.people_on_photos FOR SELECT USING (true);
 B   DROP POLICY people_on_photos_all_view ON public.people_on_photos;
       public          postgres    false    353            "           3256    919274 ,   people_on_smotrim people_on_smotrim_all_view    POLICY     ^   CREATE POLICY people_on_smotrim_all_view ON public.people_on_smotrim FOR SELECT USING (true);
 D   DROP POLICY people_on_smotrim_all_view ON public.people_on_smotrim;
       public          postgres    false    355            #           3256    919275 ,   people_on_youtube people_on_youtube_all_view    POLICY     ^   CREATE POLICY people_on_youtube_all_view ON public.people_on_youtube FOR SELECT USING (true);
 D   DROP POLICY people_on_youtube_all_view ON public.people_on_youtube;
       public          postgres    false    357            $           3256    919276 @   people_to_msegments_mapping people_to_msegments_mapping_all_view    POLICY     r   CREATE POLICY people_to_msegments_mapping_all_view ON public.people_to_msegments_mapping FOR SELECT USING (true);
 X   DROP POLICY people_to_msegments_mapping_all_view ON public.people_to_msegments_mapping;
       public          postgres    false    359            '           3256    919277 <   printed_to_people_mapping printed_to_people_mapping_all_view    POLICY     n   CREATE POLICY printed_to_people_mapping_all_view ON public.printed_to_people_mapping FOR SELECT USING (true);
 T   DROP POLICY printed_to_people_mapping_all_view ON public.printed_to_people_mapping;
       public          postgres    false    367            (           3256    919278    quotes quotes_all_view    POLICY     H   CREATE POLICY quotes_all_view ON public.quotes FOR SELECT USING (true);
 .   DROP POLICY quotes_all_view ON public.quotes;
       public          postgres    false    369                       3256    919279    people_bundles read_bundles    POLICY     M   CREATE POLICY read_bundles ON public.people_bundles FOR SELECT USING (true);
 3   DROP POLICY read_bundles ON public.people_bundles;
       public          postgres    false    346                       3256    919280    days_of_war read_days    POLICY     G   CREATE POLICY read_days ON public.days_of_war FOR SELECT USING (true);
 -   DROP POLICY read_days ON public.days_of_war;
       public          postgres    false    313                       3256    919281 "   komso_episodes read_komso_episodes    POLICY     T   CREATE POLICY read_komso_episodes ON public.komso_episodes FOR SELECT USING (true);
 :   DROP POLICY read_komso_episodes ON public.komso_episodes;
       public          postgres    false    323                       3256    919282    media_segments read_msegments    POLICY     O   CREATE POLICY read_msegments ON public.media_segments FOR SELECT USING (true);
 5   DROP POLICY read_msegments ON public.media_segments;
       public          postgres    false    328                       3256    919283    organizations read_orgs    POLICY     I   CREATE POLICY read_orgs ON public.organizations FOR SELECT USING (true);
 /   DROP POLICY read_orgs ON public.organizations;
       public          postgres    false    339                       3256    919284    people read_people    POLICY     D   CREATE POLICY read_people ON public.people FOR SELECT USING (true);
 *   DROP POLICY read_people ON public.people;
       public          postgres    false    341            %           3256    919285    photos read_photos    POLICY     D   CREATE POLICY read_photos ON public.photos FOR SELECT USING (true);
 *   DROP POLICY read_photos ON public.photos;
       public          postgres    false    363            &           3256    919286    printed read_printed    POLICY     F   CREATE POLICY read_printed ON public.printed FOR SELECT USING (true);
 ,   DROP POLICY read_printed ON public.printed;
       public          postgres    false    365            +           3256    919287 &   smotrim_episodes read_smotrim_episodes    POLICY     X   CREATE POLICY read_smotrim_episodes ON public.smotrim_episodes FOR SELECT USING (true);
 >   DROP POLICY read_smotrim_episodes ON public.smotrim_episodes;
       public          postgres    false    375            ,           3256    919288 &   telegram_authors read_telegram_authors    POLICY     X   CREATE POLICY read_telegram_authors ON public.telegram_authors FOR SELECT USING (true);
 >   DROP POLICY read_telegram_authors ON public.telegram_authors;
       public          postgres    false    377            -           3256    919289 (   telegram_channels read_telegram_channels    POLICY     Z   CREATE POLICY read_telegram_channels ON public.telegram_channels FOR SELECT USING (true);
 @   DROP POLICY read_telegram_channels ON public.telegram_channels;
       public          postgres    false    379            /           3256    919290    theory read_theory    POLICY     D   CREATE POLICY read_theory ON public.theory FOR SELECT USING (true);
 *   DROP POLICY read_theory ON public.theory;
       public          postgres    false    383            1           3256    919291 "   youtube_authors read_utube_authors    POLICY     T   CREATE POLICY read_utube_authors ON public.youtube_authors FOR SELECT USING (true);
 :   DROP POLICY read_utube_authors ON public.youtube_authors;
       public          postgres    false    387            2           3256    919292 $   youtube_channels read_utube_channels    POLICY     V   CREATE POLICY read_utube_channels ON public.youtube_channels FOR SELECT USING (true);
 <   DROP POLICY read_utube_channels ON public.youtube_channels;
       public          postgres    false    389            3           3256    919293    youtube_vids read_utube_vids    POLICY     N   CREATE POLICY read_utube_vids ON public.youtube_vids FOR SELECT USING (true);
 4   DROP POLICY read_utube_vids ON public.youtube_vids;
       public          postgres    false    391            )           3256    919294 (   rutube_channels rutube_channels_all_view    POLICY     Z   CREATE POLICY rutube_channels_all_view ON public.rutube_channels FOR SELECT USING (true);
 @   DROP POLICY rutube_channels_all_view ON public.rutube_channels;
       public          postgres    false    371            *           3256    919295     rutube_vids rutube_vids_all_view    POLICY     R   CREATE POLICY rutube_vids_all_view ON public.rutube_vids FOR SELECT USING (true);
 8   DROP POLICY rutube_vids_all_view ON public.rutube_vids;
       public          postgres    false    373            .           3256    919296    text_media text_media_all_view    POLICY     P   CREATE POLICY text_media_all_view ON public.text_media FOR SELECT USING (true);
 6   DROP POLICY text_media_all_view ON public.text_media;
       public          postgres    false    381            0           3256    919297    websites websites_all_view    POLICY     L   CREATE POLICY websites_all_view ON public.websites FOR SELECT USING (true);
 2   DROP POLICY websites_all_view ON public.websites;
       public          postgres    false    385           