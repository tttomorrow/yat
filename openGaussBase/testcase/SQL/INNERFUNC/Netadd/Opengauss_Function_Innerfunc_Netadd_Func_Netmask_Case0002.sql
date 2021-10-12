-- @testpoint: 网络地址函数netmask(inet)异常校验，合理报错

-- v4
-- 带掩码
SELECT netmask('256.168.1.5/0') AS RESULT;
SELECT netmask('192.168.1.5/33') AS RESULT;
SELECT netmask('192.168.1.5-24') AS RESULT;
SELECT netmask('192:168:1:5/25') AS RESULT;
SELECT netmask('192.168.1.5.9/32') AS RESULT;

-- 不带掩码
SELECT netmask('256.168.1.5') AS RESULT;
SELECT netmask('192:168:1') AS RESULT;
SELECT netmask('192.168.1.5.9') AS RESULT;

-- 特殊地址
SELECT netmask('0.0.0.0/3.9') AS RESULT;
SELECT netmask('255.255.255.255/0x40') AS RESULT;

-- v6
-- 带前缀
SELECT netmask('1::1::ddff/64') AS RESULT;
SELECT netmask('1::1:ddff/133') AS RESULT;
SELECT netmask('1::1:ddff-128') AS RESULT;

-- 不带前缀
SELECT netmask('00001:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT netmask('FC00::/7%') AS RESULT;
SELECT netmask('::1/0.0') AS RESULT;

SELECT netmask('::10.2.3.4:ffff') AS RESULT;
SELECT netmask('::ffff:10.4.3.2/129') AS RESULT;

-- mac
SELECT netmask('0800.2b01.0203') AS RESULT;

-- 多参少参空值
SELECT netmask('') AS RESULT;
SELECT netmask('192.168.1.5','192.1.1.1') AS RESULT;

-- cidr
SELECT netmask('192.168.100.128-25'::cidr) AS RESULT;
SELECT netmask('192.168/25':cidr) AS RESULT;
SELECT netmask('10'::cidr1) AS RESULT;
SELECT netmask('2001:4f8:3:ba::/129'::cidr) AS RESULT;
SELECT netmask('2001:4f8:3:ba:2e0:81ff:fe22:d1gh'::cidr) AS RESULT;

