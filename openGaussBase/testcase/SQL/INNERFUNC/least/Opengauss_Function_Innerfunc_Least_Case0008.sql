-- @testpoint: 数值函数嵌套的输入测试
select least(ACOS(-0.9),34) from sys_dummy;
select least(COS(120 * 3.14159265359/180),34) from sys_dummy;
select least(EXP(3.9),34) from sys_dummy;
