from django.db import models
from django.contrib.postgres.fields import ArrayField


__doc__ = """This is an auto-generated Django model module.
You'll have to do the following manually to clean this up:
 * Make sure each model has one field with primary_key=True
 * Ensure every model has `managed = False` line, if you wish to forbid Django to create, 
   modify or delete the table
 * AutoFields must set primary_key=True
 * `max_length` must be a positive integer everywhere
"""


class SixtyMinutesVids(models.Model):
    """
    60_minutes_vids
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    smotrim_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = '60_minutes_vids'
        verbose_name_plural = "SixtyMinutesVids"


class Articles(models.Model):
    """
    articles
    """
    id = models.BigAutoField(primary_key=True)
    title_ru = models.TextField(blank=True, null=True)
    book = models.ForeignKey('Books', models.DO_NOTHING, blank=True, null=True)
    title_en = models.TextField(blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    org = models.ForeignKey('Organizations', models.DO_NOTHING, blank=True, null=True)
    url = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'articles'
        verbose_name_plural = "Articles"


class ArticlesAuthors(models.Model):
    """
    """
    id = models.IntegerField(unique=True)
    person = models.OneToOneField('People', models.DO_NOTHING, primary_key=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'articles_authors'
        unique_together = (('person', 'article'),)


class BesogonVids(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    youtube_stats = models.JSONField(blank=True, null=True)
    youtube_stats_updated_on = models.DateField(blank=True, null=True)
    youtube_channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'besogon_vids'


class Books(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    title_ru = models.TextField(unique=True, blank=True, null=True)
    title_en = models.TextField(unique=True, blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    supa_url = models.TextField(unique=True, blank=True, null=True)
    year_first_published = models.SmallIntegerField(blank=True, null=True)
    meta = ArrayField(models.TextField(), blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class BooksAuthors(models.Model):
    """
    """
    person = models.OneToOneField('People', models.DO_NOTHING, primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_authors'
        unique_together = (('person', 'book'),)


class DaysOfWar(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    day_date = models.DateField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'days_of_war'


class DaytvVids(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    youtube_stats = models.JSONField(blank=True, null=True)
    youtube_stats_updated_on = models.DateField(blank=True, null=True)
    youtube_channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'daytv_vids'


class EMashMapdata(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    captured = ArrayField(models.TextField(), blank=True, null=True)
    hotspots = ArrayField(models.JSONField(), blank=True, null=True)
    day = models.OneToOneField(DaysOfWar, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e_mash_mapdata'


class KomsomolskayaPravdaVids(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    youtube_stats = models.JSONField(blank=True, null=True)
    youtube_stats_updated_on = models.DateField(blank=True, null=True)
    youtube_channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING, blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()
    need = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'komsomolskayapravda_vids'


class KtoProtivVids(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    smotrim_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey('MediaSegments', models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'kto_protiv_vids'


class MediaCoverageType(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    type_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'media_coverage_type'


class MediaRoles(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    role = models.TextField(unique=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_roles'


class MediaSegments(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    segment = models.TextField(unique=True, blank=True, null=True)
    cadence_raw = models.TextField(blank=True, null=True)
    typical_duration = models.SmallIntegerField(blank=True, null=True)
    host_present = models.SmallIntegerField(blank=True, null=True)
    parent = models.ForeignKey('Organizations', models.DO_NOTHING, db_column='parent', blank=True, null=True)
    avg_guest_time = models.SmallIntegerField(blank=True, null=True)
    segment_en = models.CharField(max_length=255, blank=True, null=True)
    smotrim_id = models.IntegerField(unique=True, blank=True, null=True)
    vesti = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'media_segments'


class MetametricaVids(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    youtube_stats = models.JSONField(blank=True, null=True)
    youtube_stats_updated_on = models.DateField(blank=True, null=True)
    youtube_channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    have = models.BooleanField()
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'metametrica_vids'


class MkpVids(models.Model):
    """
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

    class Meta:
        managed = False
        db_table = 'mkp_vids'


class OrganizationType(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    org_type = models.TextField(unique=True, blank=True, null=True)
    parent_type = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_type', blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization_type'


class Organizations(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    name_en = models.TextField(blank=True, null=True)
    name_ru = models.TextField(blank=True, null=True)
    parent_org = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    region = models.ForeignKey('RfTerritorial', models.DO_NOTHING, db_column='region', blank=True, null=True)
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
    """
    """

    id = models.BigAutoField(primary_key=True)
    fullname_en = models.TextField()
    fullname_ru = models.TextField()
    lastname_en = models.TextField(blank=True, null=True)
    lastname_ru = models.TextField(blank=True, null=True)
    is_onmap = models.BooleanField(blank=True, null=True)
    social = ArrayField(models.TextField(), blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_ttu = models.BooleanField(blank=True, null=True)
    is_ff = models.BooleanField(blank=True, null=True)
    relevant = models.BooleanField()
    contact = models.JSONField(blank=True, null=True)
    address = ArrayField(models.TextField(), blank=True, null=True)
    associates = ArrayField(models.JSONField(), blank=True, null=True)
    additional = models.JSONField(blank=True, null=True)
    aliases = ArrayField(models.JSONField(), blank=True, null=True)
    info = models.JSONField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)
    cod = models.CharField(max_length=255, blank=True, null=True)
    known_for = models.JSONField(blank=True, null=True)
    wiki_ref = models.JSONField(blank=True, null=True)
    namesake_seq = models.SmallIntegerField(blank=True, null=True)
    fullname_uk = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'people'
        unique_together = (('fullname_en', 'namesake_seq'),)
        verbose_name_plural = "Person"


class People3RdprtDetailsRaw(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    url = models.TextField()
    text_raw = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_3rdprt_details_raw'
        unique_together = (('person', 'url'),)


class PeopleBundles(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    bundle_name = models.JSONField(blank=True, null=True)
    bundle_type = models.TextField(blank=True, null=True)
    parent_bundle = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_bundles'


class PeopleInBundles(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    bundle = models.ForeignKey(PeopleBundles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'people_in_bundles'
        unique_together = (('person', 'bundle'),)


class PeopleInOrgs(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING)
    org = models.ForeignKey(Organizations, models.DO_NOTHING)
    is_active = models.BooleanField(blank=True, null=True)
    media_segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_in_control = models.BooleanField(blank=True, null=True)
    role = models.JSONField(blank=True, null=True)
    year_started = models.SmallIntegerField(blank=True, null=True)
    year_ended = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_in_orgs'


class PeopleInUr(models.Model):
    """
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
        managed = False
        db_table = 'people_in_ur'


class PeopleOnDaytv(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    episode = models.ForeignKey(DaytvVids, models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_on_daytv'
        unique_together = (('person', 'episode'),)


class PeopleOnMetametrica(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    episode = models.ForeignKey(MetametricaVids, models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_on_metametrica'
        unique_together = (('person', 'episode'),)


class PeopleOnMorningMardan(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    episode = models.ForeignKey(KomsomolskayaPravdaVids, models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_on_morning_mardan'
        unique_together = (('person', 'episode'),)


class PeopleOnPhotos(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(blank=True, null=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    photo = models.ForeignKey('Photos', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'people_on_photos'
        unique_together = (('person', 'photo'),)
        verbose_name_plural = "PeopleOnPhotos"


class PeopleOnSolovyovlive(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    episode = models.ForeignKey('SolovyovliveVids', models.DO_NOTHING)
    media_role = models.ForeignKey(MediaRoles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'people_on_solovyovlive'
        unique_together = (('person', 'episode', 'media_role'),)


class PeopleOnSolovyovvecher(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    episode = models.ForeignKey('SolovyovliveVids', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'people_on_solovyovvecher'
        unique_together = (('person', 'episode'),)


class Photos(models.Model):
    """
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


class Quotes(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    content = models.JSONField()
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    source = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quotes'


class RadioEpisodes(models.Model):
    """
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

    class Meta:
        managed = False
        db_table = 'radio_episodes'


class RfTerritorial(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True, blank=True, null=True)
    region_type = models.TextField(blank=True, null=True)
    wiki_ref = models.TextField(unique=True, blank=True, null=True)
    name_en = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rf_territorial'


class SolovyovliveVids(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    have = models.BooleanField(blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    smotrim_title = models.TextField(blank=True, null=True)
    smotrim_id = models.TextField(unique=True, blank=True, null=True)
    vk_id = models.TextField(unique=True, blank=True, null=True)
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'solovyovlive_vids'


class SolovyovvecherVids(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    timestamp_aired = models.DateTimeField(blank=True, null=True)
    url = models.TextField(unique=True, blank=True, null=True)
    have = models.BooleanField(blank=True, null=True)
    need = models.BooleanField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    smotrim_id = models.TextField(unique=True, blank=True, null=True)
    source = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    segment = models.ForeignKey(MediaSegments, models.DO_NOTHING, blank=True, null=True)
    url_is_alive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'solovyovvecher_vids'


class TelegramAuthors(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    person = models.OneToOneField(People, models.DO_NOTHING, primary_key=True)
    channel = models.ForeignKey('TelegramChannels', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'telegram_authors'
        unique_together = (('person', 'channel'),)


class TelegramChannels(models.Model):
    """
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
    restrictions = ArrayField(models.JSONField(), blank=True, null=True)
    linked_chat_id = models.BigIntegerField(blank=True, null=True)
    history_count = models.BigIntegerField(blank=True, null=True)
    last_known_message_publish_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'telegram_channels'


class TelegramChannelsStats(models.Model):
    """
    """

    id = models.IntegerField(unique=True)
    day_date = models.DateField(primary_key=True)
    stats = models.JSONField(blank=True, null=True)
    channel = models.ForeignKey(TelegramChannels, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'telegram_channels_stats'
        unique_together = (('day_date', 'channel'),)


class TypychnyVyshinskyVids(models.Model):
    """
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

    class Meta:
        managed = False
        db_table = 'typychny_vyshinsky_vids'


class VestiVids(models.Model):
    """
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

    class Meta:
        managed = False
        db_table = 'vesti_vids'


class Websites(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    url = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'websites'


class YoutubeAuthors(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey('YoutubeChannels', models.DO_NOTHING, blank=True, null=True)
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_authors'


class YoutubeChannels(models.Model):
    """
    """

    id = models.BigAutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    subs_count = models.IntegerField(blank=True, null=True)
    vids_count = models.IntegerField(blank=True, null=True)
    views_count = models.IntegerField(blank=True, null=True)
    uploads_playlist_id = models.TextField(blank=True, null=True)
    stats_updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_channels'


class YoutubeVids(models.Model):
    """
    """
    id = models.BigAutoField(primary_key=True)
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

    class Meta:
        managed = False
        db_table = 'youtube_vids'


class PeopleExtended(models.Model):
    """
    `people_extended` view
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
    cod = models.CharField(max_length=255, blank=True, null=True)
    known_for = models.JSONField(blank=True, null=True)
    wiki_ref = models.JSONField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    external_links = models.TextField(blank=True, null=True)
    bundles = models.JSONField(blank=True, null=True)
    thumb = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'people_extended'
        managed = False
