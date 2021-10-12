-- @testpoint: 网络地址函数text(inet)异常校验，合理报错

-- v4
-- 带掩码
SELECT text(inet '256.168.1.5/0') AS RESULT;
SELECT text(inet '192.168.1.5/33') AS RESULT;
SELECT text(inet '192.168.1.5-24') AS RESULT;
SELECT text('192:168:1:5/25'::inet) AS RESULT;
SELECT text('192.168.1.5.9/32'::inet) AS RESULT;

-- 不带掩码
SELECT text(inet '256.168.1.5') AS RESULT;
SELECT text(inet '192:168:1') AS RESULT;
SELECT text('192.168.1.5.9'::inet) AS RESULT;

-- 特殊地址
SELECT text('0.0.0.0/3.9'::inet) AS RESULT;
SELECT text(inet '255.255.255.255/0x40') AS RESULT;

-- v6
-- 带前缀
SELECT text(inet '1::1::ddff/64') AS RESULT;
SELECT text(inet'1::1:ddff/133') AS RESULT;
SELECT text('1::1:ddff-128'::inet) AS RESULT;

-- 不带前缀
SELECT text('00001:1:897d::ddff'::inet) AS RESULT;
-- 特殊地址
SELECT text('FC00::/7%'::inet) AS RESULT;
SELECT text(inet '::1/0.0') AS RESULT;

SELECT text(inet '::10.2.3.4:ffff') AS RESULT;
SELECT text('::ffff:10.4.3.2/129'::inet1) AS RESULT;

-- 多参少参空值
SELECT text(inet '') AS RESULT;
SELECT text('192.168.1.5','192.1.1.1') AS RESULT;

-- cidr
SELECT text('192.168.100.128-25'::cidr) AS RESULT;
SELECT text('192.168/25':cidr) AS RESULT;
SELECT text('10'::cidr1) AS RESULT;
SELECT text(cidr '2001:4f8:3:ba::/129') AS RESULT;
SELECT text(cidr '2001:4f8:3:ba:2e0:81ff:fe22:d1gh') AS RESULT;