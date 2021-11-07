---folder:Simple_db;
---sqlite3:simple.db;

--view of R table:
SELECT * FROM R;

--expected result:
--(Row)           Col1           Col2           Col3
--    1             v1             v2             v3
--    2             v4             v5             v6
SELECT
    r.A1 AS Col1,
    r.A2 AS Col2,
    r.A3 AS Col3
FROM R r;
