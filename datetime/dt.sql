--sqlite3:
select a, datetime(a), b, date(b), c, time(c) from dt;
--mysql:
select a, timestamp(a), b, date(b), c, time(c) from dt;
--postgre:
select "A", "B", date(cast("B" as TEXT)), "C" from dt;
select "A", "A"::timestamp, "B", "B"::date, "C", "C":: time from dt;
select current_date + '00:00:01'::time;
select  DATE_PART('month', "A") from dt;
--SELECT TO_TIMESTAMP("A", 'YYYYMM/DD/HH24:MI:ss') AS  new_timestamptz;
SELECT TO_TIMESTAMP("A"::text, 'YYYY-MM-DD HH24:MI:ss') AS  "A" from dt;
SELECT TO_TIMESTAMP("A"::text, 'YYYY-MM-DD HH24:MI:ss')::time AS  "A" from dt;
SELECT date(TO_TIMESTAMP("A"::text, 'YYYY-MM-DD HH24:MI:ss')) AS  "A" from dt;
SELECT TO_DATE("A"::text, 'YYYY-MM-DD') AS  "A" from dt;
SELECT TO_TIMESTAMP("C"::text, 'HH24:MI:SS')::TIME AS "C" from dt;
