drop view if exists localities_by_region cascade;
drop view if exists people_extended cascade;

drop table if exists msegments_to_rchannels_mapping cascade;
drop table if exists msegments_to_ychannels_mapping cascade;
drop table if exists people_3rdprt_details_raw cascade;
drop table if exists people_in_bundles cascade;
drop table if exists people_in_orgs cascade;
drop table if exists people_on_photos cascade;
drop table if exists people_on_smotrim cascade;
drop table if exists people_on_youtube cascade;
drop table if exists people_in_ur cascade;
drop table if exists people_to_msegments_mapping cascade;
drop table if exists printed_to_people_mapping cascade;
drop table if exists printed cascade; -- drop cascades to constraint printed_content_printed_id_fkey
drop table if exists telegram_authors cascade;
drop table if exists telegram_channels cascade;
drop table if exists people_bundles cascade;
drop table if exists photos cascade;
drop table if exists quotes cascade;
drop table if exists theory cascade;
drop table if exists media_roles cascade;
drop table if exists media_coverage_type cascade;
drop table if exists text_media cascade;
drop table if exists websites cascade;
drop table if exists rutube_vids cascade;
drop table if exists rutube_channels cascade;
drop table if exists smotrim_episodes cascade;
drop table if exists komso_episodes cascade;
drop table if exists ntv_episodes cascade;
drop table if exists dentv_episodes cascade;
drop table if exists printed_to_people_mapping cascade;
drop table if exists printed cascade;
drop table if exists telegram_authors cascade;
drop table if exists telegram_channels cascade;
drop table if exists people cascade;
drop table if exists youtube_authors cascade;
drop table if exists youtube_vids cascade;
drop table if exists youtube_channels cascade;
drop table if exists media_segments cascade;
drop table if exists organizations cascade;
drop table if exists organization_type cascade;
drop table if exists days_of_war cascade;

drop table if exists data_transcribed_content cascade;
drop table if exists data_transcribed_content_translation_en cascade;
drop table if exists data_telegram_channels_stats cascade;
drop table if exists data_telegram_messages cascade;
drop table if exists data_transcripts cascade;
drop table if exists data_printed_content cascade;

drop table if exists enums_rucr_taxonomy cascade;
drop table if exists enums_isco08_index cascade;
drop table if exists enums_theory_types cascade;
drop table if exists enums_isco08_taxonomy_closure cascade;
drop table if exists enums_orgs_taxonomy_closure cascade;
drop table if exists enums_orgs_taxonomy cascade;
drop table if exists enums_isco08_taxonomy cascade;
drop table if exists enums_bundle_types cascade;

drop table if exists future_rodniki cascade;

drop table if exists django_admin_log cascade;
drop table if exists django_migrations cascade;
drop table if exists django_session cascade;
drop table if exists django_content_type cascade;

drop table if exists auth_group_permissions cascade;
drop table if exists auth_user_groups cascade;
drop table if exists auth_user_user_permissions cascade;
drop table if exists auth_group cascade;
drop table if exists auth_permission cascade;
drop table if exists auth_user cascade;
drop table if exists django_admin_log cascade;
