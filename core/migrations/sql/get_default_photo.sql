-- returns url for default photo based on pic_type, which can be 'large' or 'thumb'
-- and patient's sex, which can be 'm' or 'f'

create or replace function get_default_photo(pic_type text, sex text)
returns text
language sql
as $$
    select
        case when pic_type = 'large' and sex = 'm'
        then (select url from public.photos where id = 1)
        when pic_type = 'thumb' and sex = 'm'
        then (select url from public.photos where id = 2)
        when pic_type = 'large' and sex = 'f'
        then (select url from public.photos where id = 3)
		when pic_type = 'thumb' and sex = 'f'
        then (select url from public.photos where id = 4)
        end;
$$;