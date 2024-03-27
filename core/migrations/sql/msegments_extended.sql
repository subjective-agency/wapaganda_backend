create or replace view msegments_extended as
	select ms.name_ru, ms.name_en, ms.name_uk, ms.cluster, ms.segment_type, ms.latest_episode_date,
		o.name_ru as parent_org,
		mss.total, mss.total_time, mss.transcribed, mss.transcribed_time, mss.have, mss.have_time
	from public.media_segments ms
	left join service.media_segments_stats mss on ms.id = mss.segment_id
	left join public.organizations o on ms.parent_org_id = o.id
	where
		ms.relevant is true
		and ms.is_defunct is not true
		and mss.day_date = (select max(day_date) from service.media_segments_stats where segment_id = ms.id)
  	group by ms.cluster, o.name_ru, ms.id
	order by ms.cluster, ms.name_ru
