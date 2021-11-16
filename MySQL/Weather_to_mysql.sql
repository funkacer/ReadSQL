---mysql:;
use moje;

DROP TABLE IF EXISTS condition_original;
CREATE TABLE condition_original (id INTEGER PRIMARY KEY,_file TEXT,_id INTEGER,city TEXT,country TEXT,
    region TEXT,chill INTEGER,direction INTEGER,speed REAL,sunrise TEXT,sunset TEXT,humidity INTEGER,
    pressure REAL,rising INTEGER,visibility REAL,pubdate TEXT,text TEXT,code INTEGER,
    temperature INTEGER,creatat TEXT,changeat TEXT);
DROP TABLE IF EXISTS forecast_original;
CREATE TABLE forecast_original (id INTEGER PRIMARY KEY,_file TEXT,_id INTEGER,condate TEXT,day TEXT,
    date TEXT,code INTEGER,low INTEGER,high INTEGER,text TEXT,creatat TEXT,changeat TEXT);


---folder:Weather\;
---sqlite3:Weather.db;
select *  from forecast_original;

---mysql:moje;
---insert:forecast_original;

select * from forecast_original;
---pause:ask;
