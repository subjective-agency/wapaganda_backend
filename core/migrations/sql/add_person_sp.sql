-- A stored procedure for atomic adding person with at least one photo
-- Example: 
-- select add_person_with_photo('1990-05-01', 'John Doe', 'Джон Доу', 'Джон Доу', '/path/to/photo.jpg');
create or replace function add_person_with_photo(
    dob date,
    fullname_en text,
    fullname_uk text,
    fullname_ru text,
    photo_path text
)
returns void
language plpgsql
as $$
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
end; $$
