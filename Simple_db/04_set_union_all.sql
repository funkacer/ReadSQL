---folder:Simple_db;
---sqlite3:simple.db;

--view of R table:
SELECT * FROM R;

--view of S table:
SELECT * FROM S;

--expected result:
--(Row)             A1             A2             A3
--    1             v1             v2             v3
--    2             v4             v5             v6
--    3             v7             v8             v9
--    4             v1             v2             v3
SELECT * FROM R
    UNION ALL
SELECT * FROM S;
