---folder:MySQL;
---sqlite3:moje.db;

drop table if exists a;

create table a (id integer , value real, label text , value2 integer);

insert into a values (1, 1.1, "12345678910Ahoj", 1);

select * from a;

---mysql:moje;

drop table if exists a;

create table a (id integer , value real, label text , value2 integer);

select * from a;

---sqlite3:moje.db;
select * from a;

---mysql:moje;
---pause:ask;
---insert:a;
select * from a;
