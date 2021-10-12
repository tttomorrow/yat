-- @testpoint: lower函数用于查询语句
drop table if exists TEST_LOWER_001;
create table TEST_LOWER_001(STR varchar(10));
insert into TEST_LOWER_001 values('TGHJ');
select lower(STR) from TEST_LOWER_001;
drop table if exists TEST_LOWER_001;