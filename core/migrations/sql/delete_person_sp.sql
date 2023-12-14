-- A stored procedure for atomic deleting person with and all ID references
create or replace function delete_person(person_id integer) returns void
language plpgsql
as $$
declare photo_id integer;
begin
    select photo_id from people_on_photos where person_id = person_id into photo_id;
    delete from people where id = person_id;
    delete from photos where id = photo_id;
    delete from people_on_photos where person_id = person_id;
    commit;
end; $$
