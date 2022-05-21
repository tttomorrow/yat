-- @testpoint: char_length函数结合数值函数使用
select char_length(ABS(-366688)) from sys_dummy;
select char_length(ACOS(-0.9)) from sys_dummy;
select char_length(COS(120 * 3.14159265359/180)) from sys_dummy;
select char_length(EXP(3.9)) from sys_dummy;
