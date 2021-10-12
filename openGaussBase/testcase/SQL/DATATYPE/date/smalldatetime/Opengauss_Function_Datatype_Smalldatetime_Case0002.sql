-- @testpoint: 输入smalldatetime日期类型上下限

drop table if exists test_smalldatetime02;
create table test_smalldatetime02 (name smalldatetime);
insert into test_smalldatetime02 values ('0001-01-01 11:22:33.456');
insert into test_smalldatetime02 values ('9999-12-31 11:22:33.456');
select * from test_smalldatetime02;
drop table test_smalldatetime02;