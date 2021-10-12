-- @testpoint: 网络地址函数abbrev(inet)把IP地址和掩码长度抽取为文本。

-- v4
-- 带掩码
SELECT abbrev(inet '192.168.1.5/0') AS RESULT;
SELECT abbrev('192.168.1.5/7'::inet) AS RESULT;
SELECT abbrev('192.168.1.5/24'::inet) AS RESULT;
SELECT abbrev(inet '192.168.1.5/25') AS RESULT;
SELECT char_length(abbrev('192.168.1.5/32'));
SELECT abbrev('192.168.1.5/32') AS RESULT;
SELECT abbrev(inet '10.1.0.0/16') AS RESULT;
-- 不带掩码
SELECT abbrev('127.0.0.1') AS RESULT;
-- 特殊地址
SELECT abbrev(inet '0.0.0.0/17') AS RESULT;
SELECT abbrev('255.255.255.255/17'::inet) AS RESULT;

-- v6
-- 带前缀
SELECT abbrev('1::1:ddff/64'::inet) AS RESULT;
SELECT abbrev(inet '1::1:ddff/89') AS RESULT;
-- 不带前缀
SELECT abbrev(inet '1:1:897d::ddff') AS RESULT;
-- 特殊地址
SELECT abbrev('::/128'::inet) AS RESULT;
SELECT abbrev(inet 'FC00::/7') AS RESULT;
SELECT abbrev('::1/128') AS RESULT;

SELECT abbrev('::10.2.3.4') AS RESULT;
SELECT abbrev(inet'::ffff:10.4.3.2/128') AS RESULT;
