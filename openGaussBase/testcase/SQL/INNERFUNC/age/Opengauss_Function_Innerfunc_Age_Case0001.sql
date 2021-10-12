-- @testpoint: •age(timestamp, timestamp)描述：将两个参数相减，并以年、月、日作为返回值。若相减值为负，则函数返回亦为负。返回值类型：interval
SELECT age(timestamp '2001-04-10', timestamp '1957-06-13') from sys_dummy;


