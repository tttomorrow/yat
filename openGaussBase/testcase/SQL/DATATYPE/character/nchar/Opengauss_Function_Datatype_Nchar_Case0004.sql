-- @testpoint: 插入正常值，字节长度设定为1

drop table if exists test_nchar_04;
create table test_nchar_04 (name nchar(1));
insert into test_nchar_04 values ('a');
select * from test_nchar_04;
drop table test_nchar_04;