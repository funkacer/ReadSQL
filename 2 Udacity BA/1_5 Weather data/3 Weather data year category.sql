\f 2 Udacity BA\1_5 Weather data;
\cs Weather data.db;

drop table if exists year_cat;

create table year_cat as select year, case

  when year >= 1750 and year < 1760 then "1750s"
  when year >= 1760 and year < 1770 then "1760s"
  when year >= 1770 and year < 1780 then "1770s"
  when year >= 1780 and year < 1790 then "1780s"
  when year >= 1790 and year < 1800 then "1790s"

  when year >= 1800 and year < 1810 then "1800s"
  when year >= 1810 and year < 1820 then "1810s"
  when year >= 1820 and year < 1830 then "1820s"
  when year >= 1830 and year < 1840 then "1830s"
  when year >= 1840 and year < 1850 then "1840s"
  when year >= 1850 and year < 1860 then "1850s"
  when year >= 1860 and year < 1870 then "1860s"
  when year >= 1870 and year < 1880 then "1870s"
  when year >= 1880 and year < 1890 then "1880s"
  when year >= 1890 and year < 1900 then "1890s"

  when year >= 1900 and year < 1910 then "1900s"
  when year >= 1910 and year < 1920 then "1910s"
  when year >= 1920 and year < 1930 then "1920s"
  when year >= 1930 and year < 1940 then "1930s"
  when year >= 1940 and year < 1950 then "1940s"
  when year >= 1950 and year < 1960 then "1950s"
  when year >= 1960 and year < 1970 then "1960s"
  when year >= 1970 and year < 1980 then "1970s"
  when year >= 1980 and year < 1990 then "1980s"
  when year >= 1990 and year < 2000 then "1990s"

  when year >= 2000 and year < 2010 then "2000s"
  when year >= 2010 and year < 2020 then "2010s"

  else "OTHER" end as "year_cat"

from global_data;

select * from year_cat;

select "year_cat", count(*)
from year_cat
group by 1;
\pda;

--id INTEGER PRIMARY KEY AUTOINCREMENT,
