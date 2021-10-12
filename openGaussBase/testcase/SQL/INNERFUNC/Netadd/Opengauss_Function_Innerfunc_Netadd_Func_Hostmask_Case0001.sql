-- @testpoint: 网络地址函数hostmask(inet)为网络构造主机掩码。

-- v4
-- 带掩码
SELECT hostmask('192.168.1.5/0') AS RESULT;
SELECT hostmask('192.168.1.5/7') AS RESULT;
SELECT hostmask('192.168.1.5/24') AS RESULT;
SELECT hostmask('192.168.1.5/25') AS RESULT;
SELECT hostmask('192.168.1.5/32') AS RESULT;
-- 不带掩码
SELECT hostmask('127.0.0.1') AS RESULT;
-- 特殊地址
SELECT hostmask('0.0.0.0/17') AS RESULT;
SELECT hostmask('255.255.255.255/17') AS RESULT;

-- v6
-- 带前缀
SELECT hostmask('1::1:ddff/64') AS RESULT;
SELECT hostmask('1::1:ddff/89') AS RESULT;
-- 不带前缀
SELECT hostmask('1:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT hostmask('::/128') AS RESULT;
SELECT hostmask('FC00::/7') AS RESULT;
SELECT hostmask('::1/128') AS RESULT;

SELECT hostmask('::10.2.3.4') AS RESULT;
SELECT hostmask('::ffff:10.4.3.2/128') AS RESULT;

-- cidr
SELECT hostmask('192.168.100.128/25'::cidr) AS RESULT;
SELECT hostmask('192.168/24'::cidr) AS RESULT;
SELECT hostmask('192.168/25'::cidr) AS RESULT;
SELECT hostmask('192.168.1'::cidr) AS RESULT;
SELECT hostmask('192.168'::cidr) AS RESULT;
SELECT hostmask('10.1.2'::cidr) AS RESULT;
SELECT hostmask('10.1'::cidr) AS RESULT;
SELECT hostmask('10'::cidr) AS RESULT;
SELECT hostmask('10.1.2.3/32'::cidr) AS RESULT;
SELECT hostmask('2001:4f8:3:ba::/64'::cidr) AS RESULT;
SELECT hostmask('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr) AS RESULT;
SELECT hostmask('::ffff:1.2.3.0/120'::cidr) AS RESULT;
SELECT hostmask(cidr '::ffff:1.2.3.0/128') AS RESULT;