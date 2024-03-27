-- A stored procedure for atomic deleting photo with all referenced IDs
create or replace function delete_photo(photo_id integer) returns void
language plpgsql
as $$
begin
    delete from photos where id = photo_id;
    delete from people_on_photos where photo_id = photo_id;
    commit;
end; $$