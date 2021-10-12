-- @testpoint: 插入特殊字符

drop table if exists test_nchar_13;
create table test_nchar_13 (name nchar(20));
insert into test_nchar_13 values ('$@#%……&*（)');
select * from test_nchar_13;
drop table test_nchar_13;