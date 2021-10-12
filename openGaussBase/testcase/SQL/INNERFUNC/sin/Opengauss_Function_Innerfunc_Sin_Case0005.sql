-- @testpoint: sin函数输入参数为null、’‘

drop table if exists TEST_SIN_03;
create table TEST_SIN_03(COL_SIN double precision);
insert into TEST_SIN_03 values(null);
insert into TEST_SIN_03 values('');

select SIN(COL_SIN) as RESULT from TEST_SIN_03;
select SIN(COL_SIN) as RESULT from TEST_SIN_03;

drop table TEST_SIN_03;