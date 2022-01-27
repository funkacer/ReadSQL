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

select
    t1.id, Airline as "AC", "Airline Name", Source as "SC", t3."Airport Name", Destination as "DC", t4."Airport Name"
    from t1_routes as t1
left join (select * from t1_airlines group by code) as t2
    on t1.airline = t2.code
left join (select * from t1_airports group by code) as t3
    on t1.source = t3.code
left join (select * from t1_airports group by code) as t4
    on t1.destination = t4.code;

select code, min("Airline Name"), max("Airline Name"), count(*) as count from t1_airlines group by code having count > 1 order by count desc;

select t1.Code, t1."Airline Name", t2.count from t1_airlines as t1
inner join (select Code, count(*) as count from t1_airlines group by code having count > 2) as t2
on t1.code = t2.code
order by count desc;

select code, min("Airport Name"), max("Airport Name"), count(*) as count from t1_airports group by code having count > 1 order by count desc;

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
\pda;

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
