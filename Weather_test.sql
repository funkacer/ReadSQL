select strftime('%Y-%m-%d', pubdate) AS day, count(*)  from condition group by 1 order by 2 desc;
select * from condition where strftime('%Y-%m-%d', pubdate) = '2020-01-17';
select count(*) from (select strftime('%Y-%m-%d', pubdate), count(*) as count from condition group by 1 having count = 24);
select distinct strftime('%Y-%m-%d', date), strftime('%Y-%m-%d', condate), min(high), max(high)  from forecast
group by 1,2  having strftime('%Y-%m-%d', date) = '2020-01-10' order by 1,2;
