-- @testpoint: 网络地址函数set_masklen(cidr,int)异常校验，合理报错
-- v4
-- 带掩码
SELECT set_masklen(cidr '256.168.1.5/0',12) AS RESULT;
SELECT set_masklen(cidr '192.168.1.5/33',12) AS RESULT;
SELECT set_masklen(cidr '192.168.1.5-24',12) AS RESULT;
SELECT set_masklen('192:168:1:5/25'::cidr,24) AS RESULT;
SELECT set_masklen('192.168.1.5.9/32'::cidr,12) AS RESULT;
SELECT set_masklen('192.168.1.5/32'::cidr,33) AS RESULT;

-- 不带掩码
SELECT set_masklen(cidr '256.168.1.5',12) AS RESULT;
SELECT set_masklen(cidr '192:168:1',12) AS RESULT;
SELECT set_masklen('192.168.1.5.9'::cidr,12) AS RESULT;

-- 特殊地址
SELECT set_masklen('0.0.0.0/3.9'::cidr,21) AS RESULT;
SELECT set_masklen(cidr '255.255.255.255/0x40',22) AS RESULT;

-- v6
-- 带前缀
SELECT set_masklen(cidr '1::1::ddff/64',66) AS RESULT;
SELECT set_masklen(cidr'1::1:ddff/133',128) AS RESULT;
SELECT set_masklen('1::1:ddff-128'::cidr,66) AS RESULT;

-- 不带前缀
SELECT set_masklen('00001:1:897d::ddff'::cidr,66) AS RESULT;
-- 特殊地址
SELECT set_masklen('FC00::/7%'::cidr,0) AS RESULT;
SELECT set_masklen(cidr '::1/0.0',66.0) AS RESULT;

SELECT set_masklen(cidr '::10.2.3.4:ffff') AS RESULT;
SELECT set_masklen('::ffff:10.4.3.2/129'::cidr1,90) AS RESULT;

-- 多参少参空值
SELECT set_masklen(cidr '') AS RESULT;
SELECT set_masklen('192.168.1.5','192.1.1.1',9) AS RESULT;


SELECT set_masklen('1::1:ddff/64'::cidr,23) AS RESULT;
SELECT set_masklen(cidr '1::1:ddff/89',23) AS RESULT;
SELECT set_masklen(cidr '192.168.1.5/0',23) AS RESULT;
SELECT set_masklen('192.168.1.5/7'::cidr,23) AS RESULT;
SELECT set_masklen('192.168.1.5/24'::cidr,23) AS RESULT;
SELECT set_masklen(cidr '192.168.1.5/25',23) AS RESULT;