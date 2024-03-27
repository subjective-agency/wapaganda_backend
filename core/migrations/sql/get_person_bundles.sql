--returns list of bundles of a given person. Bundle is a custom group
CREATE OR REPLACE FUNCTION get_person_bundles(pid int)
RETURNS jsonb[]
LANGUAGE sql
RETURNS NULL ON NULL INPUT
AS $$
  SELECT array_agg(
    jsonb_build_object(
      'id', pb.id,
      'bundle_name', pb.bundle_name,
      'bundle_type', bt.code
    )
  )
  FROM public.people_bundles pb
  LEFT JOIN public.people_in_bundles p_in_b ON pb.id = p_in_b.bundle_id
  LEFT JOIN enums.bundle_types bt on pb.bundle_type = bt.id
  WHERE p_in_b.person_id = pid;
$$;