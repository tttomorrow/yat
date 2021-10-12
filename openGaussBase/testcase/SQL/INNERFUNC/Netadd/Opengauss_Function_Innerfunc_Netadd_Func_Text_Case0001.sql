-- @testpoint: 网络地址函数text(inet)把IP地址和掩码长度抽取为文本。


-- v4
-- 带掩码
SELECT text(inet '192.168.1.5/0') AS RESULT;
SELECT text('192.168.1.5/7') AS RESULT;
SELECT text('192.168.1.5/24') AS RESULT;
SELECT text('192.168.1.5/25') AS RESULT;
SELECT char_length(text('192.168.1.5/32'));
SELECT text('192.168.1.5.9/32') AS RESULT;
-- 不带掩码
SELECT text('127.0.0.1') AS RESULT;
-- 特殊地址
SELECT text('0.0.0.0/17') AS RESULT;
SELECT text('255.255.255.255/17') AS RESULT;

-- v6
-- 带前缀
SELECT text('1::1:ddff/64') AS RESULT;
SELECT text('1::1:ddff/89') AS RESULT;
-- 不带前缀
SELECT text('1:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT text('::/128') AS RESULT;
SELECT text('FC00::/7') AS RESULT;
SELECT text('::1/128') AS RESULT;

SELECT text('::10.2.3.4') AS RESULT;
SELECT text('::ffff:10.4.3.2/128') AS RESULT;

-- cidr
SELECT text('192.168.100.128/25'::cidr) AS RESULT;
SELECT text('192.168/24'::cidr) AS RESULT;
SELECT text('192.168/25'::cidr) AS RESULT;
SELECT text('192.168.1'::cidr) AS RESULT;
SELECT text('192.168'::cidr) AS RESULT;
SELECT text('10.1.2'::cidr) AS RESULT;
SELECT text('10.1'::cidr) AS RESULT;
SELECT text('10'::cidr) AS RESULT;
SELECT text('10.1.2.3/32'::cidr) AS RESULT;
SELECT text('2001:4f8:3:ba::/64'::cidr) AS RESULT;
SELECT text('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr) AS RESULT;
SELECT text('::ffff:1.2.3.0/120'::cidr) AS RESULT;
SELECT char_length(text('::ffff:1.2.3.0/128'::cidr));