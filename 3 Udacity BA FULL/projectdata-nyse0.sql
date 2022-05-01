\f "3 Udacity BA FULL";
\r projectdata-nyse.csvx, d = ",", tq = '"', rc = True, sc = True;
\sv {'$date':"%m/%d/%Y"};
\pc;
\df f = {['Total Revenue', 'Cost of Goods Sold', 'Sales, General and Admin.', 'Research and Development',
'Other Operating Items']:"int"};
\dp$a, pu = True;
\pd10;
\q;
\#cs projectdata-nyse.dbx;
\#t nyse, True;
