-- @testpoint: 时间/日期函数age入参只含有年月
drop table if exists test_date01;
create table test_date01 (col1 timestamp with time zone,clo2 timestamp with time zone);
insert into test_date01 values ('2003-04-12','2050-04-16');
select age(clo2,col1) from test_date01;
SELECT age(timestamp '2001-04-10', timestamp '1957-06-13');
select * from test_date01;
drop table if exists test_date01;