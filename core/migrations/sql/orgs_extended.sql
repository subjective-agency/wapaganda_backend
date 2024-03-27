create or replace view orgs_extended as

  select o.id, o.name_ru, o.name_en, o.name_uk, o.short_name, otax.term org_type, get_organization_ancestors(o.id) parent_orgs, o.source_url, o.state_affiliated, get_org_people(o.id) ppl

  from public.organizations o
  left join public.people_in_orgs pio on o.id = pio.org_id
  left join enums.orgs_taxonomy otax on o.org_type = otax.id
  left join public.people p on p.id = pio.person_id

  where o.relevant is true

  group by o.name_ru, o.name_en, o.name_uk, o.source_url, o.short_name, o.state_affiliated, o.org_form, otax.term, o.id
  order by o.name_ru