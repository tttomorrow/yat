-- @testpoint: justify_interval(interval)函数传入只含有小时和月份部分的interval
SELECT JUSTIFY_INTERVAL(INTERVAL '1 MON -1 HOUR') from sys_dummy;
