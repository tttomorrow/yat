-- @testpoint: 与HAVING、ORDER BY联用
drop table if exists zsharding_tbl;
create table zsharding_tbl(C_REAL TINYINT);
select C_REAL,ASCII(ASCII('=')) from zsharding_tbl group by C_REAL,ASCII(ASCII('=')) having ASCII(ASCII('='))=54 order by C_REAL,ASCII(ASCII('='));
drop table if exists zsharding_tbl;