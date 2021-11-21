---folder:test;
---mysql:test;

show tables;

drop table if exists test3_2;

create table test3_2 (r INTEGER PRIMARY KEY AUTO_INCREMENT, id INTEGER,
    CE datetime, CB datetime, CS datetime, CO datetime, PI text, PT text, NI integer, US text,
    SS text, ST text, AT text, PD text , PU text, ZU text);

---read:test3_2.csvx;

---insert:test3_2;

---print:columns;
