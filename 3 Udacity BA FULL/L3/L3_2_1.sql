\f "3 Udacity BA FULL\L3";
\cs pp.dbx;
Select * from web_events;
Select * from sales_reps;
Select * from region;
Select * from orders;
Select * from accounts;

with t0 as (select * from orders join accounts on account_id = accounts.id join sales_reps on sales_rep_id = sales_reps.id)
select * from t0 join (select id, name as region_name from region) t1 on t0.region_id = t1.id;
\dp$a;
\g hi, [total_amt_usd], [region_name];
