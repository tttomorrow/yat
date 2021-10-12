-- @testpoint: 网络地址函数broadcast(inet)异常校验，合理报错

-- v4
-- 带掩码
SELECT broadcast('0.0.0.0/33') AS RESULT;
SELECT broadcast('127.0.0.256/0') AS RESULT;
SELECT broadcast('224.178.192.11-0') AS RESULT;
SELECT broadcast('0.0.0.0.0/25') AS RESULT;
SELECT broadcast('224-178-192-11/25') AS RESULT;
-- 不带掩码
SELECT broadcast('192.178.192.256') AS RESULT;
SELECT broadcast('192.178.192.19.1') AS RESULT;
-- 给广播地址
SELECT broadcast('255.255.255.255.255') AS RESULT;

-- v6
-- 带前缀
SELECT broadcast('1::1:ddff/129') AS RESULT;
-- 不带前缀
SELECT broadcast('1::1:ddffr') AS RESULT;
SELECT broadcast('1:1::897d::ddff') AS RESULT;
-- 特殊地址
SELECT broadcast('FC00a::/7') AS RESULT;
-- mac
SELECT broadcast('0800.2b01.0203') AS RESULT;

-- 空值
SELECT broadcast('') AS RESULT;
SELECT broadcast('192.178.192.19/32','192.178.192.19/32') AS RESULT;
SELECT broadcast() AS RESULT;

-- cidr
SELECT broadcast('192.168.100.128-25'::cidr) AS RESULT;
SELECT broadcast('192.168/25':cidr) AS RESULT;
SELECT broadcast('10'::cidr1) AS RESULT;
SELECT broadcast('2001:4f8:3:ba::/129'::cidr) AS RESULT;
SELECT broadcast('2001:4f8:3:ba:2e0:81ff:fe22:d1gh'::cidr) AS RESULT;