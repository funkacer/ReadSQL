---folder:6 SQL Queries;
---sqlite3:data.db;

SELECT
	  id,
	  Amount,
	  RANK() OVER (ORDER BY Amount desc) as rank
	FROM bill
;

SELECT
	  id,
	  Amount,
	  DENSE_RANK() OVER (ORDER BY Amount desc) as rank
	FROM bill
;
