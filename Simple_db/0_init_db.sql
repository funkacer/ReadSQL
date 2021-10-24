---folder:Simple_db;
---sqlite3:simple.db;

CREATE TABLE R (A1 char(3), A2 char(3), A3 char(3));
CREATE TABLE S (A1 char(3), A2 char(3), A3 char(3));
CREATE TABLE T (B1 char(3), B2 char(3), B3 char(3));
CREATE TABLE U (C1 char(3), C2 char(3));
CREATE TABLE V (D1 char(3), A2 char(3));

INSERT INTO R (A1, A2, A3) VALUES ('v1','v2','v3');
INSERT INTO R (A1, A2, A3) VALUES ('v4','v5','v6');
INSERT INTO S (A1, A2, A3) VALUES ('v7','v8','v9');
INSERT INTO S (A1, A2, A3) VALUES ('v1','v2','v3');
INSERT INTO T (B1, B2, B3) VALUES ('v10','v11','v12');
INSERT INTO T (B1, B2, B3) VALUES ('v13','v14','v15');
INSERT INTO U (C1, C2) VALUES ('v5','v11');
INSERT INTO U (C1, C2) VALUES ('v8','v12');
INSERT INTO V (D1, A2) VALUES ('v16','v2');
INSERT INTO V (D1, A2) VALUES ('v17','v3');

--select R:
SELECT * FROM R;

--select S:
SELECT * FROM S;

--select T:
SELECT * FROM T;

--select U:
SELECT * FROM U;

--select V:
SELECT * FROM V;
