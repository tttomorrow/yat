-- @testpoint: array_agg运算符函数测试
SELECT array_agg(1+2) FROM sys_dummy;
SELECT array_agg(8/353253*-549) FROM sys_dummy;
SELECT array_agg(8/353+253*-549) FROM sys_dummy;
