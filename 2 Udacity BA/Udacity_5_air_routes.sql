\f "2 Udacity BA";
\s "Udacity_5_air_routes.db";

drop table if exists t1_routes;
create table t1_routes (id integer primary key autoincrement, Airline text, Source text, Destination text);

drop table if exists t1_airlines;
create table t1_airlines (id integer primary key autoincrement, Code text, "Airline Name" text);

drop table if exists t1_airports;
create table t1_airports (id integer primary key autoincrement, Code text, "Airport Name" text);

\r "Udacity_5_air-routes-sfo1_routes.txt";
\i t1_routes;

\r "Udacity_5_air-routes-sfo2_airlines.txt";
\i t1_airlines;

\r "Udacity_5_air-routes-sfo3_airports.txt";
\i t1_airports;
