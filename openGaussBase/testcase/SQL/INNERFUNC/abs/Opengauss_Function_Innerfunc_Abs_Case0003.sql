-- @testpoint: 与update结合使用
drop table if exists ABS_TEST_02;
create table ABS_TEST_02(COL_ABS NUMERIC(3,2));
insert into ABS_TEST_02 VALUES(1.35);
update ABS_TEST_02 SET COL_ABS=abs(-0.767);
select COL_ABS as RESULT FROM ABS_TEST_02;
drop table if exists ABS_TEST_02;