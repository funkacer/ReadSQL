\# !POSTGRE VERSION!, tc = 103001;

\# Code from video:;
SELECT channel,
       AVG(event_count) AS avg_event_count
FROM
(SELECT strftime('%Y-%m-%d',occurred_at) AS day,
        channel,
        count(*) as event_count
   FROM web_events
   GROUP BY 1,2
   ) sub
   GROUP BY 1
   ORDER BY 2 DESC;

\# QUIZ 1:;
SELECT strftime('%Y-%m-%d',occurred_at) AS day,
       channel,
       count(*) as event_count
  FROM web_events
  GROUP BY 1,2
  ORDER BY 3 DESC;

\# QUIZ 2: (sqlite version accepts no alias, but postgre requires it);
SELECT * FROM (SELECT strftime('%Y-%m-%d',occurred_at) AS day,
       channel,
       count(*) as event_count
  FROM web_events
  GROUP BY 1,2
  ORDER BY 3 DESC);
