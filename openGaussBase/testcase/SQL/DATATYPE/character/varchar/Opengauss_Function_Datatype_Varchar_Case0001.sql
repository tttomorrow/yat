-- @testpoint: 插入空值

drop table if exists test_varchar_01;
create table test_varchar_01 (name varchar(5));
insert into test_varchar_01 values ('');
select * from test_varchar_01;
drop table test_varchar_01;