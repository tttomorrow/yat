-- @testpoint: 与GROUP BY联用
drop table if exists zsharding_tbl;
create table zsharding_tbl(C_REAL TINYINT);
select C_REAL,ASCII(ASCII('=')) from zsharding_tbl group by C_REAL,ASCII(ASCII('=')) order by C_REAL,ASCII(ASCII('='));
drop table if exists zsharding_tbl;