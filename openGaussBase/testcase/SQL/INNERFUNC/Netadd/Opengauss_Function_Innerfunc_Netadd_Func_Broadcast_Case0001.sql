-- @testpoint: 网络地址函数broadcast(inet)求网络广播地址。

-- v4
-- 带掩码
SELECT broadcast('0.0.0.0/0') AS RESULT;
SELECT broadcast('127.0.0.1/0') AS RESULT;
SELECT broadcast('224.178.192.11/0') AS RESULT;
SELECT broadcast('224.178.192.11/16') AS RESULT;
SELECT broadcast('0.0.0.0/25') AS RESULT;
SELECT broadcast('127.0.0.1/25') AS RESULT;
SELECT broadcast('224.178.192.11/25') AS RESULT;
SELECT broadcast('0.0.0.0/32') AS RESULT;
SELECT broadcast('127.0.0.1/32') AS RESULT;
SELECT broadcast('192.178.192.19/32') AS RESULT;
-- 不带掩码
SELECT broadcast('192.178.192.19') AS RESULT;
-- 给广播地址
SELECT broadcast('192.178.255.255/17') AS RESULT;
SELECT broadcast('255.255.255.255/17') AS RESULT;

-- v6
-- 带前缀
SELECT broadcast('1::1:ddff/64') AS RESULT;
-- 不带前缀
SELECT broadcast('1::1:ddff') AS RESULT;
SELECT broadcast('1:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT broadcast('::/128') AS RESULT;
SELECT broadcast('FC00::/7') AS RESULT;
SELECT broadcast('::1/128') AS RESULT;

-- cidr
SELECT broadcast('192.168.100.128/25'::cidr) AS RESULT;
SELECT broadcast('192.168/24'::cidr) AS RESULT;
SELECT broadcast('192.168/25'::cidr) AS RESULT;
SELECT broadcast('192.168.1'::cidr) AS RESULT;
SELECT broadcast('192.168'::cidr) AS RESULT;
SELECT broadcast('10.1.2'::cidr) AS RESULT;
SELECT broadcast('10.1'::cidr) AS RESULT;
SELECT broadcast('10'::cidr) AS RESULT;
SELECT broadcast('10.1.2.3/32'::cidr) AS RESULT;
SELECT broadcast('2001:4f8:3:ba::/64'::cidr) AS RESULT;
SELECT broadcast('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr) AS RESULT;
SELECT broadcast('::ffff:1.2.3.0/120'::cidr) AS RESULT;
SELECT broadcast('::ffff:1.2.3.0/128'::cidr) AS RESULT;