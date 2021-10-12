-- @testpoint: char_length函数与btrim嵌套使用
select char_length((btrim('skjafghkjashfdskf00@@','sk@' ))) from sys_dummy;
