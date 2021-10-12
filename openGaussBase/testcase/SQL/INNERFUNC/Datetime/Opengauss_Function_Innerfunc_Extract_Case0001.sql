-- @testpoint: EXTRACT函数从TIMESTAMP类型中获取最小世纪
drop table if exists test_date01;
create table test_date01 (clo1 TIMESTAMP);
insert into test_date01 values ('0001-01-01 00:00:00 AD');
select EXTRACT(CENTURY FROM clo1) from test_date01;
SELECT EXTRACT(CENTURY FROM TIMESTAMP '0001-01-01 00:00:00 AD');
drop table if exists test_date01;