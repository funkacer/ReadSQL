\f "3 Udacity BA FULL";
\r projectdata-nyse.csvx, d = ",", tq = '"', rc = True, sc = True;
\sv {'$date':"%m/%d/%Y"};
\pc;
\df f = {["Total Revenue", "Cost of Goods Sold", "Sales, General and Admin.", "Research and Development",
"Other Operating Items"]:"int"};
\dp$a, pu = True;
\pd10;
\cs projectdata-nyse.dbx;
\t nyse, True;
update nyse set "Total Revenue" = Null where "Total Revenue" = ' $-   ';
update nyse set "Cost of Goods Sold" = Null where "Cost of Goods Sold" = ' $-   ';
update nyse set "Sales, General and Admin." = Null where "Sales, General and Admin." = ' $-   ';
update nyse set "Research and Development" = Null where "Research and Development" = ' $-   ';
update nyse set "Other Operating Items" = Null where "Other Operating Items" = ' $-   ';
select distinct "Total Revenue", "Cost of Goods Sold", "Sales, General and Admin.", "Research and Development",
"Other Operating Items" from nyse;
select * from nyse;
\dp$a, pu = 1;
\t nyse, True;
select * from nyse;
\dp$a;
