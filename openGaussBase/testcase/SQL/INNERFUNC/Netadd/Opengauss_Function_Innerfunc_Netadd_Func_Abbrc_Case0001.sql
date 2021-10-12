-- @testpoint: 网络地址函数abbrev(cidr)把IP地址和掩码长度抽取为文本。

-- v4
-- 带掩码
SELECT char_length(abbrev('192.168.1.5/32'::cidr));
SELECT abbrev('192.168.1.5/32') AS RESULT;
SELECT abbrev(cidr '10.1.0.0/16') AS RESULT;
SELECT abbrev('127.0.0.1') AS RESULT;
SELECT abbrev(cidr '0.0.0.0/17') AS RESULT;

-- v6
SELECT abbrev(cidr '1:1:897d::ddff') AS RESULT;
SELECT abbrev('::/128'::cidr) AS RESULT;
SELECT abbrev(cidr 'FC00::/7') AS RESULT;
SELECT abbrev('::1/128') AS RESULT;
SELECT abbrev('::10.2.3.4') AS RESULT;
SELECT abbrev(cidr'::ffff:10.4.3.2/128') AS RESULT;

-- cidr
SELECT abbrev('192.168.100.128/25'::cidr) AS RESULT;
SELECT abbrev('192.168/24'::cidr) AS RESULT;
SELECT abbrev('192.168/25'::cidr) AS RESULT;
SELECT abbrev('192.168.1'::cidr) AS RESULT;
SELECT abbrev('192.168'::cidr) AS RESULT;
SELECT abbrev('10.1.2'::cidr) AS RESULT;
SELECT abbrev('10.1'::cidr) AS RESULT;
SELECT abbrev('10'::cidr) AS RESULT;
SELECT abbrev('10.1.2.3/32'::cidr) AS RESULT;
SELECT abbrev('2001:4f8:3:ba::/64'::cidr) AS RESULT;
SELECT abbrev('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr) AS RESULT;
SELECT abbrev('::ffff:1.2.3.0/120'::cidr) AS RESULT;
SELECT abbrev('::ffff:1.2.3.0/128'::cidr) AS RESULT;