# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.postgres.fields import ArrayField
from django.db import models


class DaysOfWar(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_date = models.DateField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'days_of_war'


class KomsoEpisodes(models.Model):
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
        managed = False
        db_table = 'komso_episodes'


class MediaCoverageType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'media_coverage_type'


class MediaRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.TextField(unique=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_roles'


class MediaSegments(models.Model):
    name_ru = models.TextField(blank=True, null=True)
    parent_org = models.ForeignKey('Organizations', models.DO_NOTHING, blank=True, null=True)
    avg_guest_time = models.SmallIntegerField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    smotrim_id = models.IntegerField(unique=True, blank=True, null=True)
    cluster = models.TextField(blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    name_uk = models.TextField(blank=True, null=True)
    is_defunct = models.BooleanField()
    segment_type = models.TextField(blank=True, null=True)
    duration_threashold = models.IntegerField(blank=True, null=True)
    latest_episode_date = models.DateTimeField(blank=True, null=True)
    komso_id = models.IntegerField(unique=True, blank=True, null=True)
    rutube_id = models.TextField(unique=True, blank=True, null=True)
    ntv_id = models.JSONField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_segments'


class MsegmentsToRchannelsMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    rutube_channel = models.ForeignKey('RutubeChannels', models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'msegments_to_rchannels_mapping'


class MsegmentsToYchannelsMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    youtube_channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'ntv_episodes'


class OrganizationType(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_type = models.TextField(unique=True, blank=True, null=True)
    parent_type = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_type', blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization_type'


class Organizations(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_en = models.TextField(blank=True, null=True)
    name_ru = models.TextField(blank=True, null=True)
    parent_org = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    region = models.BigIntegerField(blank=True, null=True)
    source_url = models.TextField(unique=True, blank=True, null=True)
    org_type = models.ForeignKey(OrganizationType, models.DO_NOTHING, blank=True, null=True)
    coverage_type = models.ForeignKey(MediaCoverageType, models.DO_NOTHING, blank=True, null=True)
    short_name = models.JSONField(blank=True, null=True)
    name_uk = models.TextField(blank=True, null=True)
    state_affiliated = models.BooleanField(blank=True, null=True)
    org_form_raw = models.TextField(blank=True, null=True)
    org_form = models.JSONField(blank=True, null=True)
    international = models.BooleanField(blank=True, null=True)
    relevant = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'organizations'


class People(models.Model):
    fullname_en = models.TextField()
    fullname_ru = models.TextField()
    lastname_en = models.TextField(blank=True, null=True)
    lastname_ru = models.TextField(blank=True, null=True)
    is_onmap = models.BooleanField(blank=True, null=True)
    social = models.TextField(blank=True, null=True)  # This field type is a guess.
    dob = models.DateField(blank=True, null=True)
    is_ttu = models.BooleanField(blank=True, null=True)
    is_ff = models.BooleanField(blank=True, null=True)
    relevant = models.BooleanField()
    contact = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # This field type is a guess.
    associates = models.TextField(blank=True, null=True)  # This field type is a guess.
    additional = models.JSONField(blank=True, null=True)
    aliases = models.TextField(blank=True, null=True)  # This field type is a guess.
    info = models.JSONField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)
    cod = models.CharField(max_length=-1, blank=True, null=True)
    known_for = models.JSONField(blank=True, null=True)
    wiki_ref = models.JSONField(blank=True, null=True)
    namesake_seq = models.SmallIntegerField(blank=True, null=True)
    fullname_uk = models.TextField(blank=True, null=True)
    added_on = models.DateTimeField()
    sex = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'
        unique_together = (('fullname_en', 'namesake_seq'),)


class People3RdprtDetailsRaw(models.Model):
    id = models.BigAutoField()
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    url = models.TextField()
    text_raw = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_3rdprt_details_raw'
        unique_together = (('person', 'url'),)


class PeopleBundles(models.Model):
    id = models.BigAutoField(primary_key=True)
    bundle_name = models.JSONField(blank=True, null=True)
    bundle_type = models.TextField(blank=True, null=True)
    parent_bundle = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_bundles'


class PeopleInBundles(models.Model):
    id = models.BigAutoField()
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    bundle = models.ForeignKey(PeopleBundles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'people_in_bundles'
        unique_together = (('person', 'bundle'),)


class PeopleInOrgs(models.Model):
    id = models.BigAutoField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    org = models.ForeignKey(Organizations, models.DO_NOTHING)
    is_active = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    is_in_control = models.BooleanField(blank=True, null=True)
    role = models.JSONField()
    year_started = models.SmallIntegerField(blank=True, null=True)
    year_ended = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_in_orgs'
        unique_together = (('person', 'org', 'is_active', 'role'),)


class PeopleInUr(models.Model):
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
        managed = False
        db_table = 'people_in_ur'


class PeopleOnPhotos(models.Model):
    id = models.BigAutoField()
    created_at = models.DateTimeField(blank=True, null=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    photo = models.ForeignKey('Photos', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'people_on_photos'
        unique_together = (('person', 'photo'),)


class PeopleOnSmotrim(models.Model):
    id = models.BigAutoField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    episode = models.ForeignKey('SmotrimEpisodes', models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'people_on_smotrim'
        unique_together = (('person', 'episode', 'media_role'),)


class PeopleOnYoutube(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    episode = models.ForeignKey('YoutubeVids', models.DO_NOTHING, blank=True, null=True)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_on_youtube'


class PeopleToMsegmentsMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_to_msegments_mapping'


class Photos(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    is_face = models.BooleanField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photos'


class Printed(models.Model):
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
        managed = False
        db_table = 'printed'


class PrintedToPeopleMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    person_raw = models.TextField(blank=True, null=True)
    printed = models.ForeignKey(Printed, models.DO_NOTHING)
    printed_piece_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'printed_to_people_mapping'


class Quotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    content = models.JSONField()
    source = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quotes'


class RutubeChannels(models.Model):
    name = models.TextField(blank=True, null=True)
    rutube_channel_id = models.TextField(unique=True, blank=True, null=True)
    rutube_channel_alias = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rutube_channels'


class RutubeVids(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    rutube_id = models.TextField(blank=True, null=True)
    rutube_channel = models.ForeignKey(RutubeChannels, models.DO_NOTHING, blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rutube_vids'


class SmotrimEpisodes(models.Model):
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
        managed = False
        db_table = 'smotrim_episodes'


class TelegramAuthors(models.Model):
    id = models.BigAutoField()
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    channel = models.ForeignKey('TelegramChannels', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'telegram_authors'
        unique_together = (('person', 'channel'),)


class TelegramChannels(models.Model):
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
    restrictions = models.TextField(blank=True, null=True)  # This field type is a guess.
    linked_chat_id = models.BigIntegerField(blank=True, null=True)
    history_count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'telegram_channels'


class Theory(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.JSONField()
    type = models.TextField(blank=True, null=True)
    excerpt = models.JSONField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)  # This field type is a guess.
    content = models.JSONField(blank=True, null=True)
    original_content_metadata = models.TextField(blank=True, null=True)  # This field type is a guess.
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'theory'


class Websites(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'websites'


class YoutubeAuthors(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING, blank=True, null=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_authors'


class YoutubeChannels(models.Model):
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
        managed = False
        db_table = 'youtube_channels'


class YoutubeVids(models.Model):
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    youtube_stats = models.JSONField(blank=True, null=True)
    youtube_stats_updated_on = models.DateField(blank=True, null=True)
    youtube_channel = models.ForeignKey(YoutubeChannels, models.DO_NOTHING)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    url_is_alive = models.BooleanField()
    have = models.BooleanField()
    need = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
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
    added_on = models.DateTimeField()
    sex = models.TextField(blank=True, null=True)
    orgs = ArrayField(models.JSONField(), blank=True, null=True)
    telegram_channels = ArrayField(models.JSONField(), blank=True, null=True)

    class Meta:
        db_table = 'people_extended'
        managed = False
