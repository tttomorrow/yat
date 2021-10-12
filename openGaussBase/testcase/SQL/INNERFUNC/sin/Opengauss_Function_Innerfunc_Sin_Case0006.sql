-- @testpoint: sin函数输入参数为特殊字符，'Infinity'、'-Infinity',合理报错


drop table if exists TEST_SIN_04;
create table TEST_SIN_04(COL_SIN double precision);
insert into TEST_SIN_04 values('infinity');
insert into TEST_SIN_04 values('-infinity');

select SIN(COL_SIN) as RESULT from TEST_SIN_04;
select SIN(COL_SIN) as RESULT from TEST_SIN_04;

drop table TEST_SIN_04;