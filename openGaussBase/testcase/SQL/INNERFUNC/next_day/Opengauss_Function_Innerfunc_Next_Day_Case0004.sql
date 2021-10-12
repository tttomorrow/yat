-- @testpoint: next_day函数输入结果跨年
select next_day('2018-12-31',1) from sys_dummy;
select next_day('2019-12-31',1) from sys_dummy;