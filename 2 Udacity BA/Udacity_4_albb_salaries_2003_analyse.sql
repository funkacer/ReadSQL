\f "2 Udacity BA";
\s "Udacity_4_albb_salaries_2003.db";

select * from t1;
\dp;


select * from t1 where (Team like "%Oakland%" or Team like "%Anaheim%") and Position like "Pitcher";
\dp;

select avg(Salary), count(*) from t1 where (Team like "%Oakland%" or Team like "%Anaheim%") and Position like "Pitcher";
