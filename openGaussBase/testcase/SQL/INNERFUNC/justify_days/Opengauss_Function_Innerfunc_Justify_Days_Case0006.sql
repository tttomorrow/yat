-- @testpoint: justify_days(interval)函数传入只含有天数部分的interval
SELECT justify_days(interval '35 days') from sys_dummy;