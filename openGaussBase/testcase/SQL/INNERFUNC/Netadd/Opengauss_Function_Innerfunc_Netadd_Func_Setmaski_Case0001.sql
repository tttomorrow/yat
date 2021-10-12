-- @testpoint: 网络地址函数set_masklen(inet, int)为inet数值设置子网掩码长度。


-- v4
-- 带掩码
SELECT set_masklen(inet '192.168.1.5/0',-0) AS RESULT;
SELECT set_masklen('192.168.1.5/0'::inet,-0) AS RESULT;
SELECT set_masklen('192.168.1.5/0',-0) AS RESULT;
SELECT set_masklen('192.168.1.5/0',0) AS RESULT;
SELECT set_masklen('192.168.1.5/7',5) AS RESULT;
SELECT set_masklen('192.168.1.5/24',16) AS RESULT;
SELECT set_masklen('192.168.1.5/25',17) AS RESULT;
SELECT set_masklen('192.168.1.5/32',32) AS RESULT;
-- 不带掩码
SELECT set_masklen('127.0.0.1',31) AS RESULT;
SELECT set_masklen('127.0.0.1',+31) AS RESULT;
SELECT set_masklen('127.0.0.1','31') AS RESULT;
SELECT set_masklen('127.0.0.1',2*3) AS RESULT;
SELECT set_masklen('127.0.0.1',(-2)*(-3)) AS RESULT;

-- 特殊地址
SELECT set_masklen('0.0.0.0',23) AS RESULT;
SELECT set_masklen('255.255.255.255',17) AS RESULT;

-- v6
-- 带前缀
SELECT set_masklen('1::1:ddff/64',0) AS RESULT;
SELECT set_masklen('1::1:ddff/89',13) AS RESULT;
SELECT set_masklen('1::1:ddff/64',9/3.7) AS RESULT;
-- 不带前缀
SELECT set_masklen('1:1:897d::ddff',127) AS RESULT;
-- 特殊地址
SELECT set_masklen('::/128',0) AS RESULT;
SELECT set_masklen('FC00::/7',127) AS RESULT;
SELECT set_masklen('::1/128',127) AS RESULT;

SELECT set_masklen('::10.2.3.4',2) AS RESULT;
SELECT set_masklen('::ffff:10.4.3.2/128',111) AS RESULT;

