---folder:Simple_db;
---sqlite3:simple.db;

--view of R table:
SELECT * FROM R;

--expected result:
--(Row)             A1             A2             A3
--    1             v4             v5             v6
SELECT * FROM R r WHERE r.A2 = 'v5';
