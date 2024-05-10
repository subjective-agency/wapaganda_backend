from django.contrib.postgres.fields import ArrayField
from django.db import models
from postgres_composite_types import CompositeType

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


class TripleLang(CompositeType):
    # https://github.com/danni/django-postgres-composite-types
    """Text value in 3 languages: en, uk, ru"""
    en = models.CharField()
    ru = models.CharField()
    uk = models.CharField()

    class Meta:
        db_type = 'triple_lang'


class EnumsRucrTaxonomy(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = TripleLang.Field()
    tags = ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True)
    xml_id = models.TextField()
    xml_data = models.JSONField()
    updated_on = models.DateTimeField()
    status = models.TextField()

    class Meta:
        managed = True
        # enums.rucr_taxonomy
        db_table = '"enums"."rucr_taxonomy"'


class EnumsBundleTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    code = models.TextField(blank=True, null=True)
    description = TripleLang.Field(blank=True, null=True)
    updated_on = models.DateTimeField()

    class Meta:
        managed = True
        # enums.bundle_types
        db_table = '"enums"."bundle_types"'


class EnumsISCOTaxonomy(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    term = TripleLang.Field(blank=True, null=True)
    isco_code = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    tasks_include = models.TextField(blank=True, null=True)
    included_occupations = models.TextField(blank=True, null=True)
    excluded_occupations = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    skill_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        # enums.isco08_taxonomy
        db_table = '"enums"."isco08_taxonomy"'


class EnumsISCOIndex(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    isco08 = models.ForeignKey(EnumsISCOTaxonomy, models.DO_NOTHING, blank=True, null=True)
    name = TripleLang.Field(blank=True, null=True)
    appended = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        # enums.isco08_index
        db_table = '"enums"."isco08_index"'


class EnumsIscoTaxonomyClosure(models.Model):
    ancestor = models.ForeignKey(
        'EnumsISCOTaxonomy',
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='descendants'  # Unique related name for ancestor's descendants
    )
    descendant = models.ForeignKey(
        'EnumsISCOTaxonomy',
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='ancestors'  # Unique related name for descendant's ancestors
    )

    class Meta:
        managed = True
        # enums.isco08_taxonomy_closure
        db_table = '"enums"."isco08_taxonomy_closure"'
        unique_together = (('ancestor', 'descendant'),)


class EnumsOrgsTaxonomy(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    term = TripleLang.Field(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        # enums.orgs_taxonomy
        db_table = '"enums"."orgs_taxonomy"'


class EnumsOrgsTaxonomyClosure(models.Model):
    ancestor = models.ForeignKey(
        'EnumsOrgsTaxonomy',
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='descendants'  # Unique related name for ancestor's descendants
    )
    descendant = models.ForeignKey(
        'EnumsOrgsTaxonomy',
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='ancestors'  # Unique related name for descendant's ancestors
    )

    class Meta:
        managed = True
        # enums.orgs_taxonomy_closure
        db_table = '"enums"."orgs_taxonomy_closure"'
        unique_together = (('ancestor', 'descendant'),)


class EnumsTheoryTypes(models.Model):
    """
    | Name | Type | Constraint type |
    | --- | --- | --- |
    | id | integer | PRIMARY KEY |
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    term = TripleLang.Field(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        # enums.theory_types
        db_table = '"enums"."theory_types"'


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


# class KomsoCategories(models.Model):
#     ...


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
    aired_on = models.DateTimeField(blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    was_downloaded = models.BooleanField(blank=True, null=True)
    need = models.BooleanField(blank=True, null=True)
    is_alive = models.BooleanField(blank=True, null=True)
    komso_url = models.TextField(unique=True, blank=True, null=True)
    direct_url = models.TextField(unique=True, blank=True, null=True)
    cluster_id = models.BigIntegerField(blank=True, null=True)
    relevance_status_id = models.BigIntegerField(blank=True, null=True)
    komso_category_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'komso_episodes'


class DenTVEpisodes(models.Model):
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
    title = models.TextField(blank=True, null=True)
    date_aired = models.DateTimeField(blank=True, null=True)
    dentv_url = models.TextField(blank=True, null=True)
    direct_url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.JSONField(blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    stats = models.JSONField(blank=True, null=True)
    comments = models.JSONField(blank=True, null=True)
    need = models.BooleanField(blank=True, null=True)
    have = models.BooleanField(blank=True, null=True)
    url_is_alive = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    youtube_rec = models.ForeignKey('YoutubeVids', models.DO_NOTHING, blank=True, null=True)
    premium = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dentv_episodes'


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
        db_table = '"enums"."media_roles"'


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
    name = TripleLang.Field()
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
    description = models.TextField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    last_scanned_on = models.DateTimeField(blank=True, null=True)

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
    aired_on = models.DateTimeField(blank=True, null=True)
    views_count = models.IntegerField(blank=True, null=True)
    timeline = models.JSONField(blank=True, null=True)
    ntv = models.IntegerField(unique=True)
    need = models.BooleanField()
    was_downloaded = models.BooleanField()
    is_alive = models.BooleanField()
    duration = models.IntegerField(blank=True, null=True)
    rutube = models.TextField(blank=True, null=True, unique=True)
    cluster_id = models.IntegerField(blank=True, null=True)
    relevance_status_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ntv_episodes'


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
    name = TripleLang.Field(blank=True, null=True)
    parent_org = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    region = models.BigIntegerField(blank=True, null=True)
    source_url = models.TextField(unique=True, blank=True, null=True)
    org_type = models.ForeignKey(EnumsOrgsTaxonomy, models.DO_NOTHING, blank=True, null=True)
    short_name = TripleLang.Field(blank=True, null=True)
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
    fullname = TripleLang.Field()
    lastname = TripleLang.Field(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    social = ArrayField(models.TextField(), blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    relevant = models.BooleanField()
    contact = models.JSONField(blank=True, null=True)
    address = ArrayField(models.TextField(), blank=True, null=True)
    associates = ArrayField(models.JSONField(), blank=True, null=True)
    additional = ArrayField(models.JSONField(), blank=True, null=True)
    aliases = ArrayField(TripleLang.Field(), blank=True, null=True)
    info = TripleLang.Field(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)
    cod = models.CharField(max_length=255, blank=True, null=True)
    known_for = TripleLang.Field(blank=True, null=True)
    wiki_ref = models.JSONField(blank=True, null=True)
    namesake_seq = models.SmallIntegerField(blank=True, null=True)
    added_on = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'people'
        unique_together = (('fullname', 'namesake_seq'),)
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
    name = TripleLang.Field(blank=True, null=True)
    bundle_type = models.ForeignKey(EnumsBundleTypes, models.DO_NOTHING)
    parent_bundle = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bundles'


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
    title = TripleLang.Field()
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
    content = TripleLang.Field()
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


# class SmotrimBrands(models.Model):
#     ...


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
    aired_on = models.DateTimeField(blank=True, null=True)
    smotrim_id = models.TextField(blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    was_downloaded = models.BooleanField()
    is_alive = models.BooleanField()
    is_relevant = models.BooleanField(blank=True, null=True)
    brand_id = models.BigIntegerField(blank=True, null=True)
    cluster_id = models.BigIntegerField(blank=True, null=True)
    relevance_status_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'smotrim_episodes'


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
    person = models.ForeignKey(People, models.DO_NOTHING)
    episode = models.ForeignKey(SmotrimEpisodes, models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_on_smotrim'
        unique_together = (('person', 'episode', 'media_role'),)


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


class TextMedia(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    first_img_data = models.JSONField(blank=True, null=True)
    source = models.ForeignKey('Websites', models.DO_NOTHING)
    additional_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = '"data"."text_media"'


class Theory(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = TripleLang.Field(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    excerpt = TripleLang.Field(blank=True, null=True)
    images = ArrayField(models.TextField(), blank=True, null=True)
    content = TripleLang.Field(blank=True, null=True)
    original_content_metadata = ArrayField(models.JSONField(), blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    translated_by = models.JSONField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

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
    alive = models.BooleanField(blank=True, null=True)
    api_url = models.TextField(unique=True)
    included = models.BooleanField(blank=True, null=True)
    item_selector = models.TextField(unique=True)
    categories = ArrayField(models.TextField())
    cats_suffix = models.TextField(unique=True)
    last_scanned_on = models.DateTimeField(blank=True, null=True)

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
    channel_created_on = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    subs_count = models.BigIntegerField(blank=True, null=True)
    vids_count = models.BigIntegerField(blank=True, null=True)
    views_count = models.BigIntegerField(blank=True, null=True)
    uploads_playlist_id = models.TextField(blank=True, null=True)
    stats_updated_on = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    last_scanned_on = models.DateTimeField(blank=True, null=True)
    target_type_id = models.BigIntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    is_relevant = models.BooleanField(blank=True, null=True)
    is_defunct = models.BooleanField(blank=True, null=True)

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
    youtube_stats = models.JSONField(blank=True, null=True)
    stats_updated_on = models.DateField(blank=True, null=True)
    youtube_channel = models.ForeignKey(YoutubeChannels, models.DO_NOTHING)
    aired_on = models.DateTimeField(blank=True, null=True)
    is_alive = models.BooleanField()
    was_downloaded = models.BooleanField()
    need = models.BooleanField(blank=True, null=True)
    private = models.BooleanField()
    views_count = models.BigIntegerField(blank=True, null=True)
    likes_count = models.BigIntegerField(blank=True, null=True)
    comments_count = models.BigIntegerField(blank=True, null=True)
    privacy_status = models.TextField(blank=True, null=True)
    is_livestream = models.BooleanField()
    auto_default_lang = models.TextField(blank=True, null=True)
    is_licensed = models.BooleanField()
    topic_categories = ArrayField(models.TextField(), blank=True, null=True)
    recording_details = models.JSONField(blank=True, null=True)
    livestream_details = models.JSONField(blank=True, null=True)
    is_deleted = models.BooleanField()
    is_rejected = models.BooleanField()
    rejection_reason = models.TextField(blank=True, null=True)
    localizations = models.JSONField(blank=True, null=True)
    blocked_in = ArrayField(models.TextField(), blank=True, null=True)
    allowed_in = ArrayField(models.TextField(), blank=True, null=True)
    cluster_id = models.BigIntegerField(blank=True, null=True)
    relevance_status_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'youtube_vids'


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
    person = models.ForeignKey(People, models.DO_NOTHING)
    episode = models.ForeignKey(YoutubeVids, models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people_on_youtube'
        unique_together = (('person', 'episode', 'media_role'),)


class PeopleExtended(models.Model):
    """
    See People Extended view
    """
    id = models.BigAutoField(primary_key=True)
    fullname = TripleLang.Field(blank=True, null=True)
    lastname = TripleLang.Field(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    social = ArrayField(models.TextField(), blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contact = models.JSONField(blank=True, null=True)
    address = ArrayField(models.TextField(), blank=True, null=True)
    associates = ArrayField(models.JSONField(), blank=True, null=True)
    additional = models.JSONField(blank=True, null=True)
    aliases = ArrayField(TripleLang.Field(), blank=True, null=True)
    info = TripleLang.Field(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)
    cod = models.TextField(max_length=255, blank=True, null=True)
    known_for = TripleLang.Field(blank=True, null=True)
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
        managed = False


class PrintedContent(models.Model):
    id = models.BigAutoField(primary_key=True)
    printed = models.ForeignKey(Printed, models.DO_NOTHING, blank=True, null=True)
    int_sequence = models.IntegerField(blank=True, null=True)
    int_id = models.IntegerField(blank=True, null=True)
    int_name = models.TextField(blank=True, null=True)
    raw_content = models.TextField(blank=True, null=True)
    parsed_content = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = '"data"."printed_content"'
        unique_together = (('printed_id', 'int_sequence'),)


class TelegramChannelsStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_date = models.DateField()
    channel = models.ForeignKey(TelegramChannels, models.DO_NOTHING, blank=True, null=True)
    stats = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = '"data"."telegram_channels_stats"'
        unique_together = (('day_date', 'channel_id'),)


class TelegramMessages(models.Model):
    id = models.BigAutoField(primary_key=True)
    origin_id = models.IntegerField(blank=True, null=True)
    channel = models.ForeignKey(TelegramChannels, models.DO_NOTHING, blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)
    date_published = models.DateTimeField(blank=True, null=True)
    date_edit = models.DateTimeField(blank=True, null=True)
    message_type = models.TextField(blank=True, null=True)
    message_subtype = models.TextField(blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    stats = models.JSONField(blank=True, null=True)
    forwarding = models.JSONField(blank=True, null=True)
    no_forwarding = models.BooleanField(blank=True, null=True)
    misc = models.JSONField(blank=True, null=True)
    signature = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        # data.telegram_messages
        db_table = '"data"."telegram_messages"'


class Transcripts(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    smotrim = models.ForeignKey(SmotrimEpisodes, models.DO_NOTHING, blank=True, null=True)
    komso = models.ForeignKey(KomsoEpisodes, models.DO_NOTHING, blank=True, null=True)
    youtube = models.ForeignKey(YoutubeVids, models.DO_NOTHING, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    lang = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    ntv = models.ForeignKey(NtvEpisodes, models.DO_NOTHING, blank=True, null=True)
    dentv = models.ForeignKey(DenTVEpisodes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = '"data"."transcripts"'


class TranscribedContent(models.Model):
    id = models.BigAutoField(primary_key=True)
    transcript = models.ForeignKey(Transcripts, models.DO_NOTHING, blank=True, null=True)
    int_sequence = models.IntegerField(blank=True, null=True)
    start_time = models.FloatField(blank=True, null=True)
    end_time = models.FloatField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = '"data"."transcribed_content"'


class TranscribedContentEn(models.Model):
    id = models.BigAutoField(primary_key=True)
    transcript = models.ForeignKey(Transcripts, models.DO_NOTHING, blank=True, null=True)
    int_sequence = models.IntegerField(blank=True, null=True)
    start_time = models.FloatField(blank=True, null=True)
    end_time = models.FloatField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = '"data"."transcribed_content_translation_en"'


class FutureRodniki(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    author_origin_id = models.IntegerField(blank=True, null=True)
    have = models.BooleanField()
    duration = models.IntegerField(blank=True, null=True)
    url_is_alive = models.BooleanField()
    available = models.BooleanField()

    class Meta:
        managed = True
        db_table = '"future"."rodniki"'


class PopularStats(models.Model):
    count_total = models.IntegerField(primary_key=True)
    count_female = models.IntegerField(primary_key=True)
    count_male = models.IntegerField(primary_key=True)
    avg_age_total = models.DurationField(primary_key=True)
    avg_age_female = models.DurationField(primary_key=True)
    avg_age_male = models.DurationField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'popular_stats'


class OrgsExtended(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = TripleLang.Field()
    short_name = TripleLang.Field()
    org_type = TripleLang.Field()
    parent_orgs = ArrayField(base_field=models.JSONField(), blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    state_affiliated = models.BooleanField()
    ppl = ArrayField(base_field=models.JSONField(), blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orgs_extended'
