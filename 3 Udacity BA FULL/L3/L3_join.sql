select accounts.*, orders.* from accounts join orders on accounts.id = orders.account_id;
select t0.*, t1.* from accounts t0 join orders t1 on t0.id = t1.account_id;
