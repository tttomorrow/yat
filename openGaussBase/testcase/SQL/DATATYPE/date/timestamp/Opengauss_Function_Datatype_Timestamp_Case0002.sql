-- @testpoint: 输入上下限

drop table if exists test_timestamp02;
create table test_timestamp02 (name timestamp);
insert into test_timestamp02 values ('0001-01-01 11:22:33.456');
insert into test_timestamp02 values ('9999-12-31 11:22:33.456');
select * from test_timestamp02;
drop table if exists test_timestamp02;