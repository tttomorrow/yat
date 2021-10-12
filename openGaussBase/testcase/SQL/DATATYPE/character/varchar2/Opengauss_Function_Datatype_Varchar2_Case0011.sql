-- @testpoint: 插入特殊字符

drop table if exists test_varchar2_11;
create table test_varchar2_11 (name varchar2(20));
insert into test_varchar2_11 values ('$@#%……&*（)');
select * from test_varchar2_11;
drop table test_varchar2_11;