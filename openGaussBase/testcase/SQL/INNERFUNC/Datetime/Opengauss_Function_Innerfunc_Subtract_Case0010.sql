-- @testpoint: interval时间间隔相减
drop table if exists test_date01;
create table test_date01 (col1 interval);
insert into test_date01 values ('1 day' );
select col1 - interval '1 hour'  from test_date01;
drop table if exists test_date01;