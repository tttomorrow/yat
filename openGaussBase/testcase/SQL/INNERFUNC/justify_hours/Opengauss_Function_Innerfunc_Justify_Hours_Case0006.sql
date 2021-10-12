-- @testpoint: justify_hours(interval)函数传入只含有小时部分的interval
SELECT JUSTIFY_HOURS(INTERVAL '27 HOURS') from sys_dummy;
