#!/bin/bash

dump_schema() {
    local schema_name="$1"

    # Dump schema
    pg_dump -h localhost -U postgres -d wapadb -p 6002 -n "$schema_name" --schema-only --verbose -F c -f "${schema_name}_schema.bin"

    # Restore schema to SQL
    pg_restore -F c --schema-only -O --file="${schema_name}_schema.sql" "${schema_name}_schema.bin"

    # Remove binary dump
    rm "${schema_name}_schema.bin"
}

# Call the function for each schema
schemas=("public" "enums" "data" "future")

for schema in "${schemas[@]}"; do
    dump_schema "$schema"
done
