-- @testpoint: 时间/日期函数age入参一个带时区一个不带时区
drop table if exists test_date01;
create table test_date01 (col1 timestamp without time zone,clo2 timestamp with time zone);
insert into test_date01 values ('2003-04-12 04:05:06','2050-04-12 20:05:06 pst');
SELECT age(timestamp '2080-04-12 04:05:06', timestamp '2050-04-12 20:05:06 pst');
select age(clo2,col1) from test_date01;
select * from test_date01;
drop table if exists test_date01;