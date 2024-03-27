-- set of functions to support retrieval of columns' descriptions

-- returns table's system identifier
create or replace function get_table_oid(table_name text)
returns int
language sql
as $$
	select objid from pg_get_object_address('table', ARRAY[table_name], '{}')
$$;

-- returns table column's subid
create or replace function get_column_subid(table_name text, column_name text)
returns int
language sql
as $$
    select objsubid from pg_get_object_address('table column', ARRAY[table_name, column_name], '{}')
$$;

-- returns comment/description of a table's column
create or replace function get_column_comment(table_name text, column_name text, out result text)
as $$
begin
  select
    *
  into
    result
  from
    col_description(get_table_oid(table_name), get_column_subid(table_name, column_name));
end;
$$ language plpgsql;

-- Example:
-- select get_column_comment('people', 'fullname_en');