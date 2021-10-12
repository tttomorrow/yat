-- @testpoint: 网络地址函数abbrev(cidr)异常校验，合理报错
-- v4
-- 带掩码
SELECT abbrev(cidr '256.168.1.5/0') AS RESULT;
SELECT abbrev(cidr '192.168.1.5/33') AS RESULT;
SELECT abbrev(cidr '192.168.1.5-24') AS RESULT;
SELECT abbrev('192:168:1:5/25'::cidr) AS RESULT;
SELECT abbrev('192.168.1.5.9/32'::cidr) AS RESULT;

-- 不带掩码
SELECT abbrev(cidr '256.168.1.5') AS RESULT;
SELECT abbrev(cidr '192:168:1') AS RESULT;
SELECT abbrev('192.168.1.5.9'::cidr) AS RESULT;

-- 特殊地址
SELECT abbrev('0.0.0.0/3.9'::cidr) AS RESULT;
SELECT abbrev(cidr '255.255.255.255/0x40') AS RESULT;

-- v6
-- 带前缀
SELECT abbrev(cidr '1::1::ddff/64') AS RESULT;
SELECT abbrev(cidr'1::1:ddff/133') AS RESULT;
SELECT abbrev('1::1:ddff-128'::cidr) AS RESULT;

-- 不带前缀
SELECT abbrev('00001:1:897d::ddff'::cidr) AS RESULT;
-- 特殊地址
SELECT abbrev('FC00::/7%'::cidr) AS RESULT;
SELECT abbrev(cidr '::1/0.0') AS RESULT;

SELECT abbrev(cidr '::10.2.3.4:ffff') AS RESULT;
SELECT abbrev('::ffff:10.4.3.2/129'::cidr1) AS RESULT;

-- 多参少参空值
SELECT abbrev(cidr '') AS RESULT;
SELECT abbrev('192.168.1.5','192.1.1.1') AS RESULT;


SELECT abbrev('1::1:ddff/64'::cidr) AS RESULT;
SELECT abbrev(cidr '1::1:ddff/89') AS RESULT;
SELECT abbrev(cidr '192.168.1.5/0') AS RESULT;
SELECT abbrev('192.168.1.5/7'::cidr) AS RESULT;
SELECT abbrev('192.168.1.5/24'::cidr) AS RESULT;
SELECT abbrev(cidr '192.168.1.5/25') AS RESULT;