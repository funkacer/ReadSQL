---use:Weather_db_20200118.db;
select * from sqlite_master;

---use:Weather.db;
DROP TABLE IF EXISTS condition;
CREATE TABLE condition (id INTEGER PRIMARY KEY AUTOINCREMENT,_id INTEGER,city TEXT,country TEXT,
    region TEXT,chill INTEGER,direction INTEGER,speed REAL,sunrise TEXT,sunset TEXT,humidity INTEGER,
    pressure REAL,rising INTEGER,visibility REAL,pubdate TEXT,text TEXT,code INTEGER,
    temperature INTEGER,creatat TEXT,changeat TEXT);
DROP TABLE IF EXISTS forecast;
CREATE TABLE forecast (id INTEGER PRIMARY KEY AUTOINCREMENT,_id INTEGER,condate TEXT,day TEXT,
    date TEXT,code INTEGER,low INTEGER,high INTEGER,text TEXT,creatat TEXT,changeat TEXT);

---use:Weather_db_20200118.db;
select * from condition;
---use:Weather.db;
---insert:condition;

---use:Weather_db_20200118.db;
select * from forecast;
---use:Weather.db;
---insert:forecast;
