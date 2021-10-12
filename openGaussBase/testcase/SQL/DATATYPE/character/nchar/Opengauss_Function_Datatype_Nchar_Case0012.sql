-- @testpoint: 插入正常值，默认字节长度
-- @modified at: 2020-11-16

drop table if exists test_nchar_12;
create table test_nchar_12 (name nchar);
insert into test_nchar_12 values ('a');
select * from test_nchar_12;
drop table test_nchar_12;
