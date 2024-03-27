-- registered_duration
-- transcription_endtime
-- transcribed_lines_count
-- translation_endtime
-- translated_lines_count


create or replace function copy_registered_duration()
returns void
returns null on null input
as $$
declare
    i int;
    tbl text;
    tbl_id int;
begin
    for i, tbl, tbl_id in
        select id, "table", table_id from service.factory_jobs_run_details where registered_duration is null
    loop
      update service.factory_jobs_run_details set registered_duration = case
        when tbl = 'smotrim_episodes' then (select duration from public.smotrim_episodes where id = tbl_id)
        when tbl = 'youtube_vids' then (select duration from public.youtube_vids where id = tbl_id)
        when tbl = 'komso_episodes' then (select duration from public.komso_episodes where id = tbl_id)
        when tbl = 'ntv_episodes' then (select duration from public.ntv_episodes where id = tbl_id)
        when tbl = 'dentv_episodes' then (select duration from public.dentv_episodes where id = tbl_id)
	  end
      where id = i;
    end loop;
end;
$$ language plpgsql;


create or replace function count_transcribed_lines()
returns void
returns null on null input
as $$
declare
    i int;
    trans_id int;
begin
    for i, trans_id in
        select id, transcript_id from service.factory_jobs_run_details where transcription_endtime is null
    loop
      update service.factory_jobs_run_details set transcription_endtime = (SELECT MAX(end_time) FROM data.transcribed_content WHERE transcript_id = trans_id),
                                                  transcribed_lines_count = (SELECT COUNT(id) FROM data.transcribed_content WHERE transcript_id = trans_id)
      where id = i;
    end loop;
end;
$$ language plpgsql;

create or replace function count_translated_lines()
returns void
returns null on null input
as $$
declare
    i int;
    trans_id int;
begin
    for i, trans_id in
        select id, transcript_id from service.factory_jobs_run_details where translation_endtime is null
    loop
      update service.factory_jobs_run_details set translation_endtime = (SELECT MAX(end_time) FROM data.transcribed_content_translation_en WHERE transcript_id = trans_id),
                                                  translated_lines_count = (SELECT COUNT(id) FROM data.transcribed_content_translation_en WHERE transcript_id = trans_id)
      where id = i;
    end loop;
end;
$$ language plpgsql;