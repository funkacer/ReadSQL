\f "2 Udacity BA";
\s "Udacity_4_albb_salaries_2003.db";

select * from t1;
\dp;

select Team, Position, sum(Salary) from t1 group by Team, Position;
\pd 100;
