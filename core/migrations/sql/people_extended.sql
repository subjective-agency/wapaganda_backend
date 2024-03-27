-- View comprises data on the relevant patients, both from the people table, and elsewhere in the DB
create or replace view people_extended as

  select p.id, p.fullname_uk, p.fullname_ru, p.fullname_en, p.lastname_en, p.lastname_ru, p.social, p.dob, p.is_ttu,
  p.is_ff, p.contact, p.address, p.associates, p.additional, p.aliases, p.info, p.dod, p.cod, p.known_for, p.wiki_ref,
  coalesce(get_person_photo(p.id, 'large'), get_default_photo('large', p.sex)) as photo,
  get_person_external_links(p.id) as external_links,
  get_person_bundles(p.id) as bundles,
  coalesce(get_person_photo(p.id, 'thumb'), get_default_photo('thumb', p.sex)) as thumb,
  added_on, get_orgs_data(get_patient_orgs_idx(p.id)) as orgs, p.sex,
  get_tchannels_data(get_patient_tchannels_idx(p.id)) as telegram_channels,
  get_ychannels_data(get_patient_ychannels_idx(p.id)) as youtube_channels
  from public.people p
  left join public.people_on_photos pop on p.id = pop.person_id
  left join public.photos ph on pop.photo_id = ph.id

  where p.relevant is true

  group by p.id, p.fullname_uk, p.fullname_ru, p.fullname_en, p.lastname_en, p.lastname_ru, p.social, p.dob, p.is_ttu,
  p.is_ff, p.contact, p.address, p.associates, p.additional, p.aliases, p.info, p.dod, p.cod, p.known_for, p.wiki_ref
  order by p.lastname_ru;
