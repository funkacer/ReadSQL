\f "3 Udacity BA FULL";
\cs projectdata-nyse.dbx;
\# tt= "Reasearch and development expenses";
with t1 as (select round(avg("Research and Development")) as "Research and Development", Years from nyse group by 2
union all
select round(avg("Research and Development")) as "Research and Development", 'Total' as Years from nyse)
select * from t1
left join
(select min("Period Ending"), max("Period Ending"), Years from nyse group by 3) t2
using(Years);
select min("Period Ending"), max("Period Ending"), Years, "Ticker symbol" from nyse group by 3,4;
select min("Period Ending")as Min, max("Period Ending") as Max, Years, "Ticker symbol" from nyse group by 3,4 having Min != Max;

select strftime("%Y", min("Period Ending")) as YearMin, strftime("%Y", max("Period Ending")) as YearMax, "Ticker symbol" from nyse group by 3;
with t1 as
(select strftime("%Y", min("Period Ending")) as YearMin, strftime("%Y", max("Period Ending")) as YearMax, "Ticker symbol" from nyse group by 3)
select "Ticker symbol", YearMin, YearMax, YearMax - YearMin as YearDiff from t1 order by 4 desc;

select strftime("%Y", min("Period Ending")) as YearMin, strftime("%Y", max("Period Ending")) as YearMax, "Ticker symbol" from nyse group by 3;
with t1 as
(select strftime("%Y", min("Period Ending")) as YearMin, strftime("%Y", max("Period Ending")) as YearMax, "Ticker symbol" from nyse group by 3)
select "Ticker symbol", YearMin, YearMax, YearMax - YearMin as YearDiff from t1 where YearDiff < 4 order by 4 desc;
