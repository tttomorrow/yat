-- @testpoint: 插入特殊字符

drop table if exists test_varchar_12;
create table test_varchar_12 (name varchar(20));
insert into test_varchar_12 values ('$@#%……&*（)');
select * from test_varchar_12;
drop table test_varchar_12;