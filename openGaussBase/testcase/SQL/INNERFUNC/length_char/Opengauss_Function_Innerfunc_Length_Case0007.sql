-- @testpoint: 字符处理函数length与数值函数嵌套测试
select length(ABS(-3435354356)) from sys_dummy;
select length(COS(120 * 3.14159265359/180)) from sys_dummy;
