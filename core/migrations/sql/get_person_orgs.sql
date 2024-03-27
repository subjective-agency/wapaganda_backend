-- returns array of orgs' IDs per given patient
create or replace function get_patient_orgs_idx(oid bigint)
returns integer ARRAY
language sql
returns null on null input
as $$
    select array_agg(o.id)
    from public.organizations o
    left join public.people_in_orgs pio on o.id = pio.org_id
    where oid = pio.person_id
$$;

CREATE OR REPLACE FUNCTION get_orgs_data(ids INT[])
  RETURNS JSONB[]
  LANGUAGE plpgsql
AS $$
DECLARE
  result JSONB[];
  record_data RECORD;
BEGIN
  FOR record_data IN
    SELECT DISTINCT ON(o.id)
    o.id id, o.name_en name_en, o.name_ru name_ru, o.name_uk name_uk,
    ot.term org_type,
    op.name_ru parent_org_name, op.id parent_org_id,
    o.source_url url, o.short_name short_name, o.state_affiliated state_aff, o.org_form org_form,
    pio.is_active active, i08t.term role_category, json_build_object('en', i08i.name_en, 'ru', i08i.name_ru, 'uk', i08i.name_uk) role_in_org
    FROM public.organizations o
    JOIN enums.orgs_taxonomy ot on ot.id = o.org_type
    JOIN public.organizations op on o.parent_org_id = op.id
    JOIN public.people_in_orgs pio on o.id = pio.org_id
    JOIN enums.isco08_taxonomy i08t on pio.role_category = i08t.id
    JOIN enums.isco08_index i08i on pio.role_ref = i08i.id
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
      'org_form', record_data.org_form,
      'active', record_data.active,
      'role_category', record_data.role_category,
      'role_in_org', record_data.role_in_org
    );

  END LOOP;

  RETURN result;
END;
$$;