---folder:Simple_db;
---sqlite3:simple.db;

--view of R table:
SELECT * FROM R;

--expected result:
--(Row)             A1             A3
--    1             v1             v3
--    2             v4             v6
SELECT A1, A3 FROM R;
