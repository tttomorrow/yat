-- @testpoint: 无效边界值测试，合理报错

drop table if exists test_smalldatetime15;
create table test_smalldatetime15 (name smalldatetime);
insert into test_smalldatetime15 values ('0000-00-00 00:00:00.000000');
select * from test_smalldatetime15;
drop table test_smalldatetime15;