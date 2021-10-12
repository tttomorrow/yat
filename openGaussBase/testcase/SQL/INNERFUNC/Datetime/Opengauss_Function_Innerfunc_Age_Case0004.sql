-- @testpoint: 时间/日期函数age，两参数都不带时区
drop table if exists test_date01;
create table test_date01 (col1 timestamp without time zone,clo2 timestamp without time zone);
insert into test_date01 values ('2003-04-13 05:07:07','2050-04-12 04:05:06');
select age(clo2,col1) from test_date01;
select * from test_date01;
drop table if exists test_date01;