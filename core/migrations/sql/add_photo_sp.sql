-- A stored procedure for atomic adding photo with one and more existing persons
-- Example: select add_photo_with_people('/path/to/photo.jpg', ARRAY[1, 3, 5]);
create or replace function add_photo_with_people(
    path text,
    person_ids integer[]
)
returns void
language plpgsql
as $$
declare photo_id integer;
declare person_id integer;
begin
    insert into photos (path)
    values (path)
    returning id into photo_id;

    foreach person_id in array person_ids
    loop
        insert into people_on_photos (person_id, photo_id)
        values (person_id, photo_id);
    end loop;

    commit;
end; $$


-- The version of the stored procedure for atomic adding photo with one or more existing persons
-- that accepts an array of person's full names in English, instead of an array of person ids
-- Please note! that this procedure assumes that fullname_en is unique in people table,
-- otherwise it will lead to unexpected results.
create or replace function add_photo_with_people_v2(
    path text,
    fullname_en text[]
)
returns void
language plpgsql
as $$
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
end; $$
