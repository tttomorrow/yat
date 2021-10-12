-- @testpoint: 网络地址函数network(inet)抽取地址的网络部分。

-- v4
-- 带掩码
SELECT network('192.168.1.5/0') AS RESULT;
SELECT network('192.168.1.5/7') AS RESULT;
SELECT network('192.168.1.5/24') AS RESULT;
SELECT network('192.168.1.5/25') AS RESULT;
SELECT network('192.168.1.5/32') AS RESULT;
-- 不带掩码
SELECT network('127.0.0.1') AS RESULT;
-- 特殊地址
SELECT network('0.0.0.0/17') AS RESULT;
SELECT network('255.255.255.255/17') AS RESULT;

-- v6
-- 带前缀
SELECT network('1::1:ddff/64') AS RESULT;
SELECT network('1::1:ddff/89') AS RESULT;
-- 不带前缀
SELECT network('1:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT network('::/128') AS RESULT;
SELECT network('FC00::/7') AS RESULT;
SELECT network('::1/128') AS RESULT;
-- cidr
SELECT network('192.168.100.128/25'::cidr) AS RESULT;
SELECT network('192.168/24'::cidr) AS RESULT;
SELECT network('192.168/25'::cidr) AS RESULT;
SELECT network('192.168.1'::cidr) AS RESULT;
SELECT network('192.168'::cidr) AS RESULT;
SELECT network('10.1.2'::cidr) AS RESULT;
SELECT network('10.1'::cidr) AS RESULT;
SELECT network('10'::cidr) AS RESULT;
SELECT network('10.1.2.3/32'::cidr) AS RESULT;
SELECT network('2001:4f8:3:ba::/64'::cidr) AS RESULT;
SELECT network('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr) AS RESULT;
SELECT network('::ffff:1.2.3.0/120'::cidr) AS RESULT;
SELECT network('::ffff:1.2.3.0/128'::cidr) AS RESULT;