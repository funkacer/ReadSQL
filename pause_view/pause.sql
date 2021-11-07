---folder:pause_view;
---sqlite3:pause.db;

drop table if exists a;

create table a (id integer primary key autoincrement, value real, label text , value2 integer);

insert into a values (Null, 1.1, "12345678910Ahoj", 1);
insert into a values (Null, 1.1, "Ahoj", 1);
  insert into a values (Null, 1.1, "Ahoj", 1);
    insert into a values (Null, 1.1, "Ahoj", 1);
      insert into a values (Null, 1.1, "Ahoj", 1);
        insert into a values (Null, 1.1, "Ahoj toto je velmi dlouhý text který neví", 1);
          insert into a values (Null, 1.1, "Ahoj", 1);
            insert into a values (Null, 1.1, "Ahoj", 1);
              insert into a values (Null, 1.1, "Ahoj", 1);
                insert into a values (Null, 1.1, "Ahoj", 1);
                  insert into a values (Null, 1.1, "Ahoj", 1);
                    insert into a values (Null, 1.1, "Ahoj", 1);
                      insert into a values (Null, 1.1, "Ahoj", 1);
                        insert into a values (Null, 1.1, "Ahoj", 1);


select * from a;

---pause:ask;

select * from b;
