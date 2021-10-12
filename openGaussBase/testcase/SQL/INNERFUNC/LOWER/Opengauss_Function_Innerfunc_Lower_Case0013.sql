-- @testpoint: lower函数作为count的入参
drop table if exists TEST_LOWER_006;
create table TEST_LOWER_006 (COL1 varchar2(20));
insert into TEST_LOWER_006 values('*');
select count(lower(COL1)) from TEST_LOWER_006 order by 1;
drop table if exists TEST_LOWER_006;