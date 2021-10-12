-- @testpoint: insert into插入结合使用
drop table if exists ABS_TEST_01;
create table ABS_TEST_01(COL_ABS int);
insert into ABS_TEST_01 values (cast(abs(-1)as int));
insert into ABS_TEST_01 values (cast(abs(99.9999)as int));
select COL_ABS AS RESULT from ABS_TEST_01;
drop table if exists ABS_TEST_01;