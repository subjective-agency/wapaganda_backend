from django.contrib.postgres.fields import ArrayField
from django.db import models


__doc__ = """This file based on auto-generated Django ORM models from the database.
You'll have to do the following edits to clean this up manually:
 * Rearrange models' order
 * Make sure each model has one field with primary_key=True
 * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
 * Ensure every model has `managed = True` line, if you wish to forbid Django to create,
   modify or delete the table
 * `max_length` must be a positive integer everywhere
 * Feel free to rename the models, but don't rename db_table values or field names
"""


class DaysOfWar(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | day_date | date | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    day_date = models.DateField(unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'days_of_war'


class KomsoEpisodes(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | direct_url | text | UNIQUE |
    | komso_id | integer | UNIQUE |
    | komso_url | text | UNIQUE |
    | segment_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    komso_id = models.IntegerField(unique=True)
    komso_seq = models.SmallIntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    have = models.BooleanField(blank=True, null=True)
    need = models.BooleanField(blank=True, null=True)
    url_is_alive = models.BooleanField(blank=True, null=True)
    komso_url = models.TextField(unique=True, blank=True, null=True)
    direct_url = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'komso_episodes'


class MediaCoverageType(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | type_name | text | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    type_name = models.TextField(unique=True)

    class Meta:
        managed = True
        db_table = 'media_coverage_type'


class MediaRoles(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | role | text | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    role = models.TextField(unique=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'media_roles'


class MediaSegments(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | UNIQUE, PRIMARY KEY |
    | komso_id | integer | UNIQUE |
    | rutube_id | text | UNIQUE |
    | smotrim_id | integer | UNIQUE |
    | parent_org_id | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    name_en = models.TextField(blank=True, null=True)
    name_ru = models.TextField(blank=True, null=True)
    name_uk = models.TextField(blank=True, null=True)
    parent_org = models.ForeignKey('Organizations', models.DO_NOTHING, blank=True, null=True)
    avg_guest_time = models.SmallIntegerField(blank=True, null=True)
    smotrim_id = models.IntegerField(unique=True, blank=True, null=True)
    cluster = models.TextField(blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    is_defunct = models.BooleanField()
    segment_type = models.TextField(blank=True, null=True)
    duration_threshold = models.IntegerField(blank=True, null=True)
    latest_episode_date = models.DateTimeField(blank=True, null=True)
    komso_id = models.IntegerField(unique=True, blank=True, null=True)
    rutube_id = models.TextField(unique=True, blank=True, null=True)
    ntv_id = models.JSONField(unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'media_segments'


class MsegmentsToRchannelsMapping(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | media_segment_id | bigint | FOREIGN KEY |
    | rutube_channel_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    rutube_channel = models.ForeignKey('RutubeChannels', models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'msegments_to_rchannels_mapping'


class MsegmentsToYchannelsMapping(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | media_segment_id | bigint | FOREIGN KEY |
    | youtube_channel_id | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    youtube_channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'msegments_to_ychannels_mapping'


class NtvEpisodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    timeline = models.JSONField(blank=True, null=True)
    ntv_id = models.IntegerField(unique=True)
    need = models.BooleanField()
    have = models.BooleanField()
    url_is_alive = models.BooleanField()
    duration = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ntv_episodes'


class OrganizationType(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | org_type | text | UNIQUE |
    | parent_type | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    org_type = models.TextField(unique=True, blank=True, null=True)
    parent_type = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_type', blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'organization_type'


class Organizations(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | UNIQUE PRIMARY KEY |
    | source_url | text | UNIQUE |
    | coverage_type_id | bigint | FOREIGN KEY |
    | org_type_id | bigint | FOREIGN KEY |
    | parent_org_id | bigint | FOREIGN KEY |
    | region | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    name_en = models.TextField(blank=True, null=True)
    name_ru = models.TextField(blank=True, null=True)
    name_uk = models.TextField(blank=True, null=True)
    parent_org = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    region = models.BigIntegerField(blank=True, null=True)
    source_url = models.TextField(unique=True, blank=True, null=True)
    org_type = models.ForeignKey(OrganizationType, models.DO_NOTHING, blank=True, null=True)
    coverage_type = models.ForeignKey(MediaCoverageType, models.DO_NOTHING, blank=True, null=True)
    short_name = models.JSONField(blank=True, null=True)
    state_affiliated = models.BooleanField(blank=True, null=True)
    org_form_raw = models.TextField(blank=True, null=True)
    org_form = models.JSONField(blank=True, null=True)
    international = models.BooleanField(blank=True, null=True)
    relevant = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'organizations'


class People(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | fullname_en | text | UNIQUE |
    | fullname_en | text | UNIQUE |
    | namesake_seq | smallint | UNIQUE |
    | namesake_seq | smallint | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    fullname_en = models.TextField()
    fullname_ru = models.TextField()
    fullname_uk = models.TextField(blank=True, null=True)
    lastname_en = models.TextField(blank=True, null=True)
    lastname_ru = models.TextField(blank=True, null=True)
    is_onmap = models.BooleanField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    social = ArrayField(models.TextField(), blank=True, null=True)  # This field type is a guess.
    dob = models.DateField(blank=True, null=True)
    is_ttu = models.BooleanField(blank=True, null=True)
    is_ff = models.BooleanField(blank=True, null=True)
    relevant = models.BooleanField()
    contact = models.JSONField(blank=True, null=True)
    address = ArrayField(models.TextField(), blank=True, null=True)
    associates = ArrayField(models.JSONField(), blank=True, null=True)  # This field type is a guess.
    additional = ArrayField(models.JSONField(), blank=True, null=True)
    aliases = ArrayField(models.JSONField(), blank=True, null=True)  # This field type is a guess.
    info = models.JSONField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)
    cod = models.CharField(max_length=255, blank=True, null=True)
    known_for = models.JSONField(blank=True, null=True)
    wiki_ref = models.JSONField(blank=True, null=True)
    namesake_seq = models.SmallIntegerField(blank=True, null=True)
    added_on = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'people'
        unique_together = (('fullname_en', 'namesake_seq'),)
        verbose_name_plural = "Person"


class People3RdprtDetailsRaw(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | person_id | integer | PRIMARY KEY |
    | url | text | PRIMARY KEY |
    | person_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.OneToOneField(People, models.DO_NOTHING)
    url = models.TextField()
    text_raw = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_3rdprt_details_raw'
        unique_together = (('person', 'url'),)


class PeopleBundles(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | parent_bundle_id | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    bundle_name = models.JSONField(blank=True, null=True)
    bundle_type = models.TextField(blank=True, null=True)
    parent_bundle = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_bundles'


class PeopleInBundles(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | person_id | integer | PRIMARY KEY, FOREIGN KEY |
    | bundle_id | bigint | PRIMARY KEY, FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.OneToOneField(People, models.DO_NOTHING)
    bundle = models.ForeignKey(PeopleBundles, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'people_in_bundles'
        unique_together = (('person', 'bundle'),)


class PeopleInOrgs(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | UNIQUE |
    | person_id | integer | PRIMARY KEY |
    | org_id | bigint | PRIMARY KEY |
    | is_active | boolean | PRIMARY KEY |
    | role | jsonb | PRIMARY KEY |
    | org_id | bigint | FOREIGN KEY |
    | person_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.OneToOneField(People, models.DO_NOTHING)
    org = models.ForeignKey(Organizations, models.DO_NOTHING)
    is_active = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    is_in_control = models.BooleanField(blank=True, null=True)
    role = models.JSONField()
    year_started = models.SmallIntegerField(blank=True, null=True)
    year_ended = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_in_orgs'
        unique_together = (('person', 'org', 'is_active', 'role'),)


class PeopleInUr(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | url | text | UNIQUE |
    | person_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    in_higher_council = models.BooleanField(blank=True, null=True)
    in_higher_council_bureau = models.BooleanField(blank=True, null=True)
    in_general_council = models.BooleanField(blank=True, null=True)
    in_general_council_presidium = models.BooleanField(blank=True, null=True)
    in_general_council_presidium_commission = models.BooleanField(blank=True, null=True)
    in_central_executive_committee = models.BooleanField(blank=True, null=True)
    is_gosduma_deputy = models.BooleanField(blank=True, null=True)
    is_senator = models.BooleanField(blank=True, null=True)
    in_ethics_commission = models.BooleanField(blank=True, null=True)
    in_coordination_councils_leadership = models.BooleanField(blank=True, null=True)
    in_central_fans_council = models.BooleanField(blank=True, null=True)
    in_central_control_commission = models.BooleanField(blank=True, null=True)
    in_international_aff_commission = models.BooleanField(blank=True, null=True)
    url = models.TextField(unique=True, blank=True, null=True)
    ur_text = models.TextField(blank=True, null=True)
    is_secretary = models.BooleanField(blank=True, null=True)
    person = models.ForeignKey(People, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'people_in_ur'


class PeopleOnPhotos(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | person_id | integer | PRIMARY KEY, FOREIGN KEY |
    | photo_id | bigint | PRIMARY KEY, FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    person = models.OneToOneField(People, models.DO_NOTHING)
    photo = models.ForeignKey('Photos', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'people_on_photos'
        unique_together = (('person', 'photo'),)


class PeopleOnSmotrim(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | UNIQUE |
    | person_id | integer | PRIMARY KEY, FOREIGN KEY |
    | episode_id | integer | PRIMARY KEY, FOREIGN KEY |
    | media_role_id | bigint | PRIMARY KEY, FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.OneToOneField(People, models.DO_NOTHING)
    episode = models.ForeignKey('SmotrimEpisodes', models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'people_on_smotrim'
        unique_together = (('person', 'episode', 'media_role'),)


class PeopleOnYoutube(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | episode_id | integer | FOREIGN KEY |
    | media_role_id | bigint | FOREIGN KEY |
    | person_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    episode = models.ForeignKey('YoutubeVids', models.DO_NOTHING, blank=True, null=True)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_on_youtube'


class PeopleToMsegmentsMapping(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | media_segment_id | integer | FOREIGN KEY |
    | person_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_to_msegments_mapping'


class Photos(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    is_face = models.BooleanField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'photos'
        verbose_name_plural = "Photos"


class Printed(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | storage_ref | uuid | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    title_ru = models.TextField(blank=True, null=True)
    title_en = models.TextField(blank=True, null=True)
    title_uk = models.TextField(blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file_details = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    storage_ref = models.UUIDField(unique=True, blank=True, null=True)
    int_review = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'printed'


class PrintedToPeopleMapping(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | person_id | integer | FOREIGN KEY |
    | printed_id | bigint | FOREIGN KEY |
    | printed_piece_id | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    person_raw = models.TextField(blank=True, null=True)
    printed = models.ForeignKey(Printed, models.DO_NOTHING)
    printed_piece_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'printed_to_people_mapping'


class Quotes(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | UNIQUE PRIMARY KEY |
    | person_id | integer | FOREIGN KEY |
    | source_id | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    content = models.JSONField()
    source = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'quotes'


class RutubeChannels(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | rutube_channel_id | text | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    rutube_channel_id = models.TextField(unique=True, blank=True, null=True)
    rutube_channel_alias = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rutube_channels'


class RutubeVids(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | media_segment_id | integer | FOREIGN KEY |
    | rutube_channel_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    rutube_id = models.TextField(blank=True, null=True)
    rutube_channel = models.ForeignKey(RutubeChannels, models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rutube_vids'


class SmotrimEpisodes(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | smotrim_id | text | UNIQUE |
    | segment_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    smotrim_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()
    need = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'smotrim_episodes'


class TelegramAuthors(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | person_id | integer | PRIMARY KEY, FOREIGN KEY |
    | channel_id | integer | PRIMARY KEY, FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    person = models.OneToOneField(People, models.DO_NOTHING)
    channel = models.ForeignKey('TelegramChannels', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'telegram_authors'
        unique_together = (('person', 'channel'),)


class TelegramChannels(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | telemetr_id | text | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    telemetr_id = models.TextField(unique=True, blank=True, null=True)
    telemetr_url = models.TextField(blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    population_checked_on = models.DateTimeField(blank=True, null=True)
    handle = models.TextField(unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField()
    origin_id = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_restricted = models.BooleanField(blank=True, null=True)
    is_fake = models.BooleanField(blank=True, null=True)
    is_scam = models.BooleanField(blank=True, null=True)
    no_forward = models.BooleanField(blank=True, null=True)
    restrictions = ArrayField(models.TextField(), blank=True, null=True)  # This field type is a guess.
    linked_chat_id = models.BigIntegerField(blank=True, null=True)
    history_count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'telegram_channels'


class Theory(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.JSONField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    excerpt = models.JSONField(blank=True, null=True)
    images = ArrayField(models.TextField(), blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    original_content_metadata = ArrayField(models.JSONField(), blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'theory'


class Websites(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | url | text | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    url = models.TextField(unique=True)

    class Meta:
        managed = True
        db_table = 'websites'


class YoutubeAuthors(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | channel_id | bigint | FOREIGN KEY |
    | person_id | integer | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING, blank=True, null=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'youtube_authors'


class YoutubeChannels(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | bigint | PRIMARY KEY |
    | youtube_id | text | UNIQUE |
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    subs_count = models.BigIntegerField(blank=True, null=True)
    vids_count = models.BigIntegerField(blank=True, null=True)
    views_count = models.BigIntegerField(blank=True, null=True)
    uploads_playlist_id = models.TextField(blank=True, null=True)
    stats_updated_on = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'youtube_channels'


class YoutubeVids(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    | youtube_id | text | UNIQUE |
    | segment_id | integer | FOREIGN KEY |
    | youtube_channel_id | bigint | FOREIGN KEY |
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    youtube_channel = models.ForeignKey(YoutubeChannels, models.DO_NOTHING)
    url_is_alive = models.BooleanField()
    have = models.BooleanField()
    need = models.BooleanField(blank=True, null=True)
    private = models.BooleanField()
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    youtube_stats = models.JSONField(blank=True, null=True)
    youtube_stats_updated_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'youtube_vids'


class PeopleExtended(models.Model):
    """
    See People Extended view
    """
    id = models.BigAutoField(primary_key=True)
    fullname_uk = models.TextField(blank=True, null=True)
    fullname_en = models.TextField()
    fullname_ru = models.TextField()
    lastname_en = models.TextField(blank=True, null=True)
    lastname_ru = models.TextField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    social = ArrayField(models.TextField(), blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_ttu = models.BooleanField(blank=True, null=True)
    is_ff = models.BooleanField(blank=True, null=True)
    contact = models.JSONField(blank=True, null=True)
    address = ArrayField(models.TextField(), blank=True, null=True)
    associates = ArrayField(models.JSONField(), blank=True, null=True)
    additional = models.JSONField(blank=True, null=True)
    aliases = ArrayField(models.JSONField(), blank=True, null=True)
    info = models.JSONField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)
    cod = models.TextField(max_length=255, blank=True, null=True)
    known_for = models.JSONField(blank=True, null=True)
    wiki_ref = models.JSONField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    external_links = ArrayField(models.TextField(), blank=True, null=True)
    bundles = ArrayField(models.JSONField(), blank=True, null=True)
    thumb = models.TextField(blank=True, null=True)
    orgs = ArrayField(models.JSONField(), blank=True, null=True)
    telegram_channels = ArrayField(models.JSONField(), blank=True, null=True)
    youtube_channels = ArrayField(models.JSONField(), blank=True, null=True)
    added_on = models.DateTimeField()

    class Meta:
        db_table = 'people_extended'
        managed = True
