#!/bin/bash
# Restore wapadb without service tables

snaplet snapshot restore --exclude-tables auth.audit_log_entries auth.identities auth.instances auth.mfa_amr_claims auth.mfa_challenges auth.mfa_factors auth.refresh_tokens auth.saml_providers auth.saml_relay_states auth.schema_migrations auth.sessions auth.sso_domains auth.sso_providers auth.users auth.flow_state supabase_migrations.schema_migrations supabase_function.hooks supabase_function.migrations cron.job cron.job_run_details
