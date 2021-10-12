-- @testpoint: trunc函数入参给数字表示的时间段
drop table if exists test_date01;
create table test_date01 (clo1 numeric);
insert into test_date01 values ('31.25');
select trunc(clo1) from test_date01;
SELECT trunc(numeric '99.99');
drop table if exists test_date01;