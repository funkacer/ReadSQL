\f "2 Udacity BA";
\s "Udacity_4_worldcities.db";

select max("All") as "All", max(Dist) as Dist, max("All") - max(Dist) as Diff from(
select count(*) as "All", 0 as Dist from t1
union all
select 0 As "All", count(*) as Dist from (select distinct City, Country from t1));
