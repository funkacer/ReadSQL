\sqlite3 :memory: ;
\read test.txt ;
create table a (id int, value real, code text) ;

\insert a ;
