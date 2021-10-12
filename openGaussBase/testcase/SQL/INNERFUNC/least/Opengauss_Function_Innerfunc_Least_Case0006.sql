-- @testpoint: 有效值测试 参数类型不同
select least('14541.2353212','sdsdsdaffdfsfdfdff','发大幅度发斯蒂芬');
-- 字符型+整数型
select least('1412','129',12) from sys_dummy;
-- 浮点型+字符型
select least('14541.2353212','独山大道') from sys_dummy;