-- @testpoint: 有效边界值测试

drop table if exists test_smalldatetime01;
create table test_smalldatetime01 (name smalldatetime);
insert into test_smalldatetime01 values ('0001-01-01 00:00:00.000000');
insert into test_smalldatetime01 values ('9999-12-31 23:59:59.999999');
select * from test_smalldatetime01;
drop table test_smalldatetime01;