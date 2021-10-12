-- @testpoint: next_day函数入参为null
select next_day('2020-06-13',null) from sys_dummy;
select next_day(null,1) from sys_dummy;
select next_day(null,null) from sys_dummy;