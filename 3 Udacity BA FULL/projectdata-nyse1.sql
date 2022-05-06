\f "3 Udacity BA FULL";
\cs projectdata-nyse.dbx;
select * from nyse;
\dp$a;
with t2 as (select "Ticker Symbol" as "Ticker Symbol Year" from nyse where Years = 'Year 1')
select distinct "Ticker Symbol" from nyse
 left join t2
 on "Ticker Symbol" = "Ticker Symbol Year"
 where "Ticker Symbol Year" is Null;
with t2 as (select "Ticker Symbol" as "Ticker Symbol Year" from nyse where Years = 'Year 2')
select distinct "Ticker Symbol" from nyse
 left join t2
 on "Ticker Symbol" = "Ticker Symbol Year"
 where "Ticker Symbol Year" is Null;
with t2 as (select "Ticker Symbol" as "Ticker Symbol Year" from nyse where Years = 'Year 3')
select distinct "Ticker Symbol" from nyse
 left join t2
 on "Ticker Symbol" = "Ticker Symbol Year"
 where "Ticker Symbol Year" is Null;
with t2 as (select "Ticker Symbol" as "Ticker Symbol Year" from nyse where Years = 'Year 4')
select distinct "Ticker Symbol" from nyse
 left join t2
 on "Ticker Symbol" = "Ticker Symbol Year"
 where "Ticker Symbol Year" is Null;

-- why not working?;
with t2 as (select "Ticker Symbol" from nyse where Years = 'Year 4')
select distinct "Ticker Symbol" from nyse t1
 left join t2
 on t1."Ticker Symbol" = t2."Ticker Symbol"
 where t2."Ticker Symbol" is Null;

with t2 as (select "Ticker Symbol" from nyse where Years = 'Year 4')
select distinct "Ticker Symbol" from nyse
 left join t2
 using("Ticker Symbol")
 where t2."Ticker Symbol" is Null;

select distinct t1."Ticker Symbol" from nyse t1
 left join (select "Ticker Symbol" from nyse where Years = 'Year 4') t2
 using("Ticker Symbol")
 where t2."Ticker Symbol" is Null;

select distinct t1."Ticker Symbol" from nyse t1
 left join (select "Ticker Symbol" from nyse where Years = 'Year 4') t2
 on t1."Ticker Symbol" = t2."Ticker Symbol"
 where t2."Ticker Symbol" is Null;
