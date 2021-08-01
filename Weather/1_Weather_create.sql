---use:Weather.db;
DROP TABLE IF EXISTS condition;
CREATE TABLE condition (id INTEGER PRIMARY KEY AUTOINCREMENT,_file TEXT,_id INTEGER,city TEXT,country TEXT,
    region TEXT,chill INTEGER,direction INTEGER,speed REAL,sunrise TEXT,sunset TEXT,humidity INTEGER,
    pressure REAL,rising INTEGER,visibility REAL,pubdate TEXT,text TEXT,code INTEGER,
    temperature INTEGER,creatat TEXT,changeat TEXT);
DROP TABLE IF EXISTS forecast;
CREATE TABLE forecast (id INTEGER PRIMARY KEY AUTOINCREMENT,_file TEXT,_id INTEGER,condate TEXT,day TEXT,
    date TEXT,code INTEGER,low INTEGER,high INTEGER,text TEXT,creatat TEXT,changeat TEXT);

---use:Weather_db_20200118.db;
select '20200118.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;
---use:Weather.db;
---insert:condition;

---use:Weather_db_20200118.db;
select '20200118.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;
---use:Weather.db;
---insert:forecast;

---use:Weather_db_20200621.db;
select '20200621.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;
---use:Weather.db;
---insert:condition;

---use:Weather_db_20200621.db;
select '20200621.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;
---use:Weather.db;
---insert:forecast;

---use:Weather_db_20201025.db;
select '20201025.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;
---use:Weather.db;
---insert:condition;

---use:Weather_db_20201025.db;
select '20201025.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;
---use:Weather.db;
---insert:forecast;

---use:Weather_db_20210307.db;
select '20210307.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;
---use:Weather.db;
---insert:condition;

---use:Weather_db_20210307.db;
select '20210307.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;
---use:Weather.db;
---insert:forecast;

---use:Weather_db_20210609.db;
select '20210609.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;
---use:Weather.db;
---insert:condition;

---use:Weather_db_20210609.db;
select '20210609.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;
---use:Weather.db;
---insert:forecast;

-- smazat 4 zaznamy z condition;
---use:Weather.db;
