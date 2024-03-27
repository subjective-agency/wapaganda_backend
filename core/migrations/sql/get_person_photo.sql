-- returns url to the user-specific photo. pic_type can be 'large' or 'thumb'
create or replace function get_person_photo(pid int, pic_type text)
returns text
language sql
returns null on null input
as $$
    select ph.url
    from public.photos ph
    left join public.people_on_photos pop on pop.photo_id = ph.id
    left join public.people p on pop.person_id = p.id
    where p.id = pid and ph.type = pic_type
$$;