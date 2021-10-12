-- @testpoint: EXTRACT函数从只有年月日的date类型中获取世纪
drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('0001-01-01');
select EXTRACT(CENTURY FROM  clo1) from test_date01;
SELECT EXTRACT(CENTURY FROM date '0001-01-01');
drop table if exists test_date01;