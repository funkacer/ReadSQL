---folder:6 SQL Queries;
---sqlite3:data.db;

SELECT id
		 , month
		 , type
		 , Amount
		 , SUM(Amount) OVER (ORDER BY id) as total_sum
		FROM bill;
