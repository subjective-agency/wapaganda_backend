-- returns array of patients' IDs per given organization
create or replace function get_org_people(oid bigint)
returns integer ARRAY
language sql
returns null on null input
as $$
    select array_agg(p.id)
    from public.people p
    left join public.people_in_orgs pio on p.id = pio.person_id
    where oid = pio.org_id
$$;



create or replace function get_org_people(oid bigint)
returns array JSONB
language sql
returns null on null input
as $$
    select json_agg(p.id id, p.fullname_en name, iindex.name_en role)
    from public.people p
    left join public.people_in_orgs pio on p.id = pio.person_id
	left join enums.isco08_index iindex on pio.role_ref1 = iidnex.id
    where oid = pio.org_id
$$;
