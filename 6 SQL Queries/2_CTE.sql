---folder:6 SQL Queries;
---sqlite3:data.db;

-- Without CTE:
SELECT *
	FROM bill
	WHERE id in
	  (SELECT DISTINCT id
	   FROM bill
	   WHERE type = "F"
	   AND month = "2021-03-01"
	  )
;

-- With CTE:
WITH idtempp as (
	SELECT DISTINCT id
	 FROM bill
	 WHERE type = "F"
	 AND month = "2021-03-01"
	)

	SELECT *
	FROM bill
	WHERE id in (SELECT id from idtempp)
;
