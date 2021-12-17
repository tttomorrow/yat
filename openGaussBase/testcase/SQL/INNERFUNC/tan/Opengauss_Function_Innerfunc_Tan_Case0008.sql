-- @testpoint: 数字操作函数，正切函数，函数嵌套

select tan(tan(tan(1234567890)))from sys_dummy;
select tan(tan(tan(tan(1234567789)))) <> 0;
select tan(ABS(-3435354356)) from sys_dummy;
select tan(ACOS(-0.9)) from sys_dummy;
select tan(COS(120 * 3.14159265359/180)) from sys_dummy;
select tan(EXP(3.9)) from sys_dummy;