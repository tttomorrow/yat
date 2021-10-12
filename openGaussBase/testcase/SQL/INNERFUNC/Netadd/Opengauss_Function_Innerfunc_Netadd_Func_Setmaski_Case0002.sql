-- @testpoint: 网络地址函数set_masklen(inet, int)异常校验，合理报错

-- v4
-- 带掩码

SELECT set_masklen('192.168.1.5/0',-0.000) AS RESULT;
SELECT set_masklen('192.168.1.5/0',-3) AS RESULT;
SELECT set_masklen('192.168.1.5/7',-7.9) AS RESULT;
SELECT set_masklen('192.168.1.5/24',16.1234) AS RESULT;
SELECT set_masklen('192.168.1.5/25',0x17) AS RESULT;
SELECT set_masklen('192.168.1.5/32',33) AS RESULT;
SELECT set_masklen(inet1 '192.168.1.5/0',-0) AS RESULT;
SELECT set_masklen('192.168.1.5/0'::inet,true) AS RESULT;
SELECT set_masklen('192.168.1.5/0'::inet, yes) AS RESULT;
SELECT set_masklen('192.168.1.5/0'::inet,'false') AS RESULT;
-- 不带掩码
SELECT set_masklen('127.0.0.1','+31.987') AS RESULT;
SELECT set_masklen('127.0.0.1',(-2)*(3)) AS RESULT;

-- 特殊地址
SELECT set_masklen('0.0.0.0',234) AS RESULT;
SELECT set_masklen('255.255.255.256',17) AS RESULT;

-- v6
-- 带前缀
SELECT set_masklen('1::1:ddff/64',-9/3.7) AS RESULT;
SELECT set_masklen('1::1:ddff/89',129) AS RESULT;
-- 不带前缀
SELECT set_masklen('1:1:897d::ddff', ) AS RESULT;
SELECT set_masklen('1:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT set_masklen('::/128',0,9) AS RESULT;
SELECT set_masklen('FC00::/7',127,1) AS RESULT;

SELECT set_masklen('::10.2.3.4','') AS RESULT;
-- 此处验证text转换int时函数校验前缀长度
SELECT set_masklen('::ffff:10.4.3.2/128','129'::text) AS RESULT;
