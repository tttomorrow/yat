-- @testpoint: last_day函数输入多个参数，合理报错
select last_day(to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'),null) from sys_dummy;
select last_day(to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'),null,1111) from sys_dummy;