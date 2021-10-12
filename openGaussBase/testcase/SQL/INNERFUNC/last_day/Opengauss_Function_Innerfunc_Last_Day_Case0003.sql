-- @testpoint: last_day函数与cast结合使用
select cast(last_day('2019-01-03 14:58:54') as varchar(1024)) from sys_dummy;
select last_day(cast('2019-01-03 14:58:54' as date)) from sys_dummy;
