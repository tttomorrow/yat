-- @testpoint: 插入正常范围值

drop table if exists test_varchar_04;
create table test_varchar_04 (name varchar(20));
insert into test_varchar_04 values ('abcdef');
select * from test_varchar_04;
drop table test_varchar_04;