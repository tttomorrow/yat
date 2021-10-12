-- @testpoint: date_trunc(text, timestamp)函数截取到参数text指定的精度。返回值类型：timestamp
SELECT date_trunc('hour', timestamp  '2001-02-16 20:38:40') from sys_dummy;