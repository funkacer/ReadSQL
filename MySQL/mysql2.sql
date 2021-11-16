---folder:MySQL;
---sqlite3:moje.db;

drop table if exists a;

create table a (id integer , value real, label text , value2 text);

insert into a values (2, 1.1, "ěščřžýáíů", "2021-11-15 13:45:27");

select * from a;

---mysql:moje;

drop table if exists a;

create table a (id integer NOT NULL AUTO_INCREMENT, value real, label text , value2 datetime, PRIMARY KEY (id)) ;
---DEFAULT CHARSET="utf8";

select * from a;

---sqlite3:moje.db;
select value, label, value2 from a;

---mysql:moje;
---insert:a;

---sqlite3:moje.db;
select value, label, value2 from a;

---mysql:moje;
---insert:a;

select * from a;

---pause:ask;
