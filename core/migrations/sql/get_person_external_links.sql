-- returns array of urls from people_3rdprt_details_raw table for a given person
create or replace function get_person_external_links(pid int)
returns text ARRAY
language sql
returns null on null input
as $$
  select string_to_array(replace(replace(url, '{', ''), '}', ''), ',')
  from public.people_3rdprt_details_raw
  where person_id = pid
$$;