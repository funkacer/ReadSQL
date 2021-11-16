---folder:MySQL;
---mysql:moje;

drop schema if exists moje;

create schema moje;

use moje;

drop table if exists a;

create table a (id integer , value real, label text , value2 integer);

insert into a values (1, 1.1, "12345678910Ahoj", 1);

select * from a;
