\f "2 Udacity BA\1_5 Weather data";
\cs "Weather data.db";

--drop table if exists city_data;
\r city_data.csv, ",";
\dp$a;
\t city_data ,  , id;

\r city_list.csv, ",";
\dp$a;
\t city_list ,  , id;

\r global_data.csv, ",";
\dp$a;
\t global_data ,  , id;
