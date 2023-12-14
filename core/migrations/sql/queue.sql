CREATE OR REPLACE FUNCTION enqueue_job(command_text text)
RETURNS integer AS $$
DECLARE
    job_id integer;
BEGIN
    INSERT INTO service.job_queue (command) VALUES (command_text) RETURNING id INTO job_id;
    RETURN job_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION process_job()
RETURNS void AS $$
    from datetime import datetime
    selectq = plpy.prepare("SELECT * FROM service.job_queue WHERE status = 'queued' ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1;")
    upd_status_proc = plpy.prepare("UPDATE service.job_queue SET status = 'processing', started_on = $1 WHERE id = $2;", ["timestamp", "int",])
    upd_status_compl = plpy.prepare("UPDATE service.job_queue SET status = 'completed', finished_on = $1 WHERE id = $2;", ["timestamp", "int",])
    upd_status_fld = plpy.prepare("UPDATE service.job_queue SET status = 'failed', failed_on = $1, fail_details = $2 WHERE id = $3;", ["timestamp", "text", "int",])
    selection = plpy.execute(selectq)
    if selection:
        start_time = datetime.now()
        plpy.execute(upd_status_proc, [start_time, selection[0]["id"]])
        try:
            exec_q = plpy.prepare(selection[0]["command"])
            plpy.execute(exec_q)
            end_time = datetime.now()
            plpy.execute(upd_status_compl, [end_time, selection[0]["id"]])
        except plpy.SPIError as e:
            fail_time = datetime.now()
            plpy.execute(upd_status_fld, [fail_time, str(e), selection[0]["id"]])
$$ LANGUAGE plpython3u;
