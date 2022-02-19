\f fill;
\r ccc.txtx;
\cs ccc.dbx;

drop table if exists t2;
drop table if exists t3;

create table t2 ('Row' INTEGER PRIMARY KEY AUTOINCREMENT,
'CRM_MKTELM' text, 'CRM_MKTELMT' text, 'CRM_CRD_AT' text, 'TYP' text, 'KOMODITA' text, 'PRODUKT' text, 'KANAL' text, 'MESIC_UKONCENÍ' int, 'VYPOVED' text, 'kc_ukar' text, 'báze' int);

\df f = {['MESIC_UKONCENÍ', 'báze']:int.};

\i t2;

select * from t2;

\pda n = [TYP];

select TYP, count(*) as count from t2 group by 1 order by 2 desc;

select TYP, count(*) as count,
CASE
	WHEN TYP IS NULL THEN '#Chybí'
	ELSE TYP
END AS TYP_KAT
 from t2 group by 1 order by 2 desc;

select
CASE
	WHEN TYP IS NULL THEN '#Chybí'
	ELSE '#NeChybí'
END AS TYP,
count(*) as count
 from t2 group by 1 order by 2 desc;

CREATE TABLE t3 AS select * from t2;

UPDATE t3 set TYP = '#Chybí' WHERE TYP IS NULL;

select * from t3;

\pd l = [540,158,159];

select TYP, count(*) as count from t3 group by 1 order by 2 desc;

\pda;

select * from t2
WHERE TYP IS NULL
;

\df n={TYP:#Chybí};

\q;
