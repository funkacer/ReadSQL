\f "2 Udacity BA";
\s "Udacity_5_air_routes.db";

select
    t1.id, Airline as "AC", "Airline Name", Source as "SC", t3."Airport Name", Destination as "DC", t4."Airport Name"
    from t1_routes as t1
left join t1_airlines as t2
    on t1.airline = t2.code
left join t1_airports as t3
    on t1.source = t3.code
left join t1_airports as t4
    on t1.destination = t4.code;

\p d l = [1,2,3,4,5,-5,-4,-3,-2,-1] tt = "Routes with Airline Names and Airport Names With Duplicities:" nt = "There should be 249 rows but is 340.
Please check duplicities carefully!!!";

select
    t1.id, Airline as "AC", "Airline Name", Source as "SC", t3."Airport Name", Destination as "DC", t4."Airport Name"
    from t1_routes as t1
left join (select * from t1_airlines group by code) as t2
    on t1.airline = t2.code
left join (select * from t1_airports group by code) as t3
    on t1.source = t3.code
left join (select * from t1_airports group by code) as t4
    on t1.destination = t4.code;

\p d l = [1,2,3,4,5,-5,-4,-3,-2,-1] tt = "Routes with Airline Names and Airport Names, No Duplicities:" nt = "There should be 249 rows. Is it OK?
Let's check duplicities in next tables!!!";

select code, min("Airline Name"), max("Airline Name"), count(*) as count from t1_airlines group by code having count > 1 order by count desc;
\p d a tt = "Airlines with more than one name:" nt = "Lets check those with 3 names thoroughly.";

select t1.Code, t1."Airline Name", t2.count from t1_airlines as t1
inner join (select Code, count(*) as count from t1_airlines group by code having count > 2) as t2
on t1.code = t2.code
order by count desc;

\p d a tt = "Airlines with three names:" nt = "I will deduplicate it with first Airline Name only.";

select code, min("Airport Name"), max("Airport Name"), count(*) as count from t1_airports group by code having count > 1 order by count desc;
\p d a tt = "Airport with more than one name - probably due to different code schemas (use wiki for HND):",
nt = "I will deduplicate it with first Airport Name only.";

select t2.id, t1.AC, t1.Count, t2."Airline Name", t2."SAirport Name", t2."SC", t2."DAirport Name", t2."DC" from
(select Airline as "AC", count(*) as Count from t1_routes group by Airline) as t1
inner join
(select
    t1.id, Airline as "AC", "Airline Name", Source as "SC", t3."Airport Name" as "SAirport Name", Destination as "DC", t4."Airport Name" as "DAirport Name"
    from t1_routes as t1
left join (select * from t1_airlines group by code) as t2
    on t1.airline = t2.code
left join (select * from t1_airports group by code) as t3
    on t1.source = t3.code
left join (select * from t1_airports group by code) as t4
    on t1.destination = t4.code) as t2
on t1.AC = t2.AC
inner join (select code, count(*) as count from t1_airports group by code having count > 1 order by count desc) as t5
on t2.DC = t5.code
order by t1.Count DESC;

\p d a tt = "Check duplicated Airport Names for destination codes:",
nt = "??? __It is questionable if HND is Henderson in case of Japan Airlines__ ???",
nc = 1001;

select * from t1_routes  as t1
inner join (select code, count(*) as count from t1_airports group by code having count > 1 order by count desc) as t2
on t1.destination = t2.code;

\p d a tt = "Check duplicated Airport Names for destination codes from t1_routes table:";

select t2.id, t1.AC, t1.Count, t2."Airline Name", t2."SAirport Name", t2."SC", t2."DAirport Name", t2."DC" from
(select Airline as "AC", count(*) as Count from t1_routes group by Airline) as t1
inner join
(select
    t1.id, Airline as "AC", "Airline Name", Source as "SC", t3."Airport Name" as "SAirport Name", Destination as "DC", t4."Airport Name" as "DAirport Name"
    from t1_routes as t1
left join (select * from t1_airlines group by code) as t2
    on t1.airline = t2.code
left join (select * from t1_airports group by code) as t3
    on t1.source = t3.code
left join (select * from t1_airports group by code) as t4
    on t1.destination = t4.code) as t2
on t1.AC = t2.AC
order by t1.Count DESC;

\p d a tt = "Final table:";
\dp;

\p d tt = "Delta should have 17 flights, so let's check it!";

select t2.id, t1.AC, t1.Count, t2."Airline Name", t2."SAirport Name", t2."SC", t2."DAirport Name", t2."DC" from
(select Airline as "AC", count(*) as Count from t1_routes group by Airline) as t1
inner join
(select
    t1.id, Airline as "AC", "Airline Name", Source as "SC", t3."Airport Name" as "SAirport Name", Destination as "DC", t4."Airport Name" as "DAirport Name"
    from t1_routes as t1
left join (select * from t1_airlines group by code) as t2
    on t1.airline = t2.code
left join (select * from t1_airports group by code) as t3
    on t1.source = t3.code
left join (select * from t1_airports group by code) as t4
    on t1.destination = t4.code) as t2
on t1.AC = t2.AC
where t1.Count = 17;

\p d a tt = "Delta should have 17 flights, so let's check it!" nt = "Looks OK :)";
