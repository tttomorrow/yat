-- @testpoint: 时间/日期函数age相减为负数
drop table if exists test_date01;
create table test_date01 (col1 timestamp with time zone,clo2 timestamp with time zone);
insert into test_date01 values ('2060-04-12 04:05:06','2050-04-12 20:05:06 pst');
select age(clo2,col1) from test_date01;
SELECT age(timestamp '2050-04-12 20:05:06 pst', timestamp '2060-04-12 04:05:06');
select * from test_date01;
drop table if exists test_date01;