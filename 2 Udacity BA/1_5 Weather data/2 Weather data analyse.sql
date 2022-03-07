\f 2 Udacity BA\1_5 Weather data;
\cs Weather data.db;

select * from city_data as t1
left join
global_data as t2
on t1.year = t2.year;

select * from
(select t1.'id' as 'country_id', t1.'year' as 'country_year', t1.'city' as 'country_city', t1.'country' as 'country_country',
t1.'avg_temp' as 'country_avg_temp'  from city_data as t1) as t1
left join
(select t1.'id' as 'global_id', t1.'year' as 'global_year', t1.'avg_temp' as 'global_avg_temp' from global_data as t1) as t2
on t1.country_year = t2.global_year;
\dp$a;
