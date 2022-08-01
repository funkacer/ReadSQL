\# !POSTGRE VERSION!, tc = 103001;

\# Code from video:;
SELECT channel,
       AVG(event_count) AS avg_event_count
FROM
(SELECT DATE_TRUNC('day',occurred_at) AS day,
        channel,
        count(*) as event_count
   FROM web_events
   GROUP BY 1,2
   ) sub
   GROUP BY 1
   ORDER BY 2 DESC;

\# QUIZ 1:;
SELECT DATE_TRUNC('day',occurred_at) AS day,
       channel,
       count(*) as event_count
  FROM web_events
  GROUP BY 1,2
  ORDER BY 3 DESC;

\# QUIZ 2:;
SELECT * FROM (SELECT DATE_TRUNC('day',occurred_at) AS day,
       channel,
       count(*) as event_count
  FROM web_events
  GROUP BY 1,2
  ORDER BY 3 DESC) sub;
