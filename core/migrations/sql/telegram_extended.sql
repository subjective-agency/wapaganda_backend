create or replace view telegram_extended AS

    select tc.id, tc.handle, tc.title, tc.telemetr_id, tc.telemetr_url, tc.population, tc.date_created created, tc.description,
           tc.history_count, tc.status, ARRAY_AGG(jsonb_build_object('id', p.id, 'fullname_en', p.fullname_en)) AS associated_ppl
    from public.telegram_channels tc
    left join public.telegram_authors ta on tc.id = ta.channel_id
    left join public.people p on ta.person_id = p.id
    where tc.relevant is TRUE and tc.title is not NULL
    GROUP BY
        tc.id, tc.handle, tc.title, tc.telemetr_id, tc.telemetr_url, tc.population, tc.date_created, tc.description,
        tc.history_count, tc.status;
    ORDER BY
        tc.id