-- Run this script after restoring a backup to fix the permissions on the database schema 
-- on DO servers only!
create or replace function create_role_if_not_exists(role_name text)
returns void as $$
begin
    role_name := lower(role_name);
    if not exists (select from pg_roles where rolname = role_name) then
        execute format('CREATE ROLE %I', role_name);
    end if;
end;
$$ language plpgsql;

create schema if not exists "auth";
create schema if not exists "extensions";

SELECT create_role_if_not_exists('anon');
SELECT create_role_if_not_exists('service_role');
SELECT create_role_if_not_exists('authenticated');

grant usage on schema public to postgres, anon, authenticated, service_role;
grant usage on schema extensions to postgres, anon, authenticated, service_role;

grant all privileges on all tables in schema public to postgres, anon, authenticated, service_role;
grant all privileges on all functions in schema public to postgres, anon, authenticated, service_role;
grant all privileges on all sequences in schema public to postgres, anon, authenticated, service_role;

alter default privileges in schema public grant all on tables to postgres, anon, authenticated, service_role;
alter default privileges in schema public grant all on functions to postgres, anon, authenticated, service_role;
alter default privileges in schema public grant all on sequences to postgres, anon, authenticated, service_role;

alter role anon set statement_timeout = '3s';
alter role authenticated set statement_timeout = '8s';
