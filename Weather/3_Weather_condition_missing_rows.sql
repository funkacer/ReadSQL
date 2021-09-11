---folder:Weather;
---sqlite3:Weather.db;
select row_number() OVER (ORDER BY id) AS row_number, id, _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate, text,
 code, temperature, creatat, changeat from condition;
with t0 AS (select row_number() OVER (ORDER BY id) AS row_number, id, _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate, text,
 code, temperature, creatat, changeat from condition)
 select row_number - id AS diff, id, _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate, text,
  code, temperature, creatat, changeat from t0 where diff < 0  group by diff order by id;
---print:columns;
--odhali duplicity
select distinct strftime('%Y-%m-%d %H', pubdate), count(*) from condition group by 1 order by 2 desc;

---sqlite3:Weather_db_20200118.db;
select '20200118.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;

---sqlite3:Weather_db_20200118.db;
--select '20200118.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;

---sqlite3:Weather_db_20200621.db;
select '20200621.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;

---sqlite3:Weather_db_20200621.db;
--select '20200621.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;

---sqlite3:Weather_db_20201025.db;
select '20201025.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;

---sqlite3:Weather_db_20201025.db;
--select '20201025.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;

---sqlite3:Weather_db_20210307.db;
select '20210307.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;

---sqlite3:Weather_db_20210307.db;
--select '20210307.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;

---sqlite3:Weather_db_20210609.db;
select '20210609.db' as _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate
, text, code, temperature, creatat, changeat from condition;

---sqlite3:Weather_db_20210609.db;
--select '20210609.db' as _file, _id, condate, day, date, code, low, high, text, creatat, changeat from forecast;

---sqlite3:Weather.db;
with t0 AS (select row_number() OVER (ORDER BY id) AS row_number, id, _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate, text,
 code, temperature, creatat, changeat from condition)
 select row_number - id AS diff, row_number, id from t0 where diff < 0  group by diff order by id;

select * from condition_original where id in (10889,13857,16334);

select * from condition where id = 10889;
select * from condition where id = 13857;
select * from condition where id = 16334;

-- druhy chybejici pro -3:
select * from condition where id = 13856;

-- tyto chybi:
select * from condition_original where id in (10889,13856,13857,16334);

-- tyto duplicity vybiram, beru jen druhou:
select * from condition_original where pubdate = '2020-10-25 08:00:00';

-- tyto duplicity vybiram, beru jen druhou:
select * from condition where id in (13856, 13858);

-- tyto duplicity maji cisla 13856 a 13858 (mezi nimi je jeden chybny zaznam co taky mazu), beru jen 13858:
select * from condition_original where id in (13856, 13857, 13858);

-- mazu posledni zaznam z 20201025 (duplicita s druhym zaznamem z 20210307) a prvni z 20201025, 20210307, 20200621
-- tj. z 20201025 mazu prvni a posledni zaznam (udela -1 a -2)
-- z 20210307 mazu prvni zaznam udela -3 (nasleduje hned po -2)
-- z 20200621 mazu prvni zaznam (udela -4)
-- a toto jsou ty hledane dva po sobe smazane zaznamy:
select * from condition_original where id in (13856, 13857);

with t0 AS (select row_number() OVER (ORDER BY id) AS row_number, id, _file, _id, city, country, region, chill, direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, pubdate, text,
 code, temperature, creatat, changeat from condition)
 select row_number - id AS diff, row_number, id from t0 where diff < 0  group by diff order by id;
