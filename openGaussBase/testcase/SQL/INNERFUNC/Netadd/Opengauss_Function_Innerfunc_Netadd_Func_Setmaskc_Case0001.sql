-- @testpoint: 网络地址函数set_masklen(cidr,int)把IP地址和掩码长度抽取为文本。

-- v4
-- 带掩码
SELECT set_masklen('192.168.1.0/24'::cidr, 32) AS RESULT;
SELECT set_masklen('192.168.1.5/32',31) AS RESULT;
SELECT set_masklen(cidr '10.1.0.0/16',0) AS RESULT;
SELECT set_masklen('127.0.0.1',9) AS RESULT;
SELECT set_masklen(cidr '0.0.0.0/17',22) AS RESULT;
SELECT char_length(host(set_masklen('192.168.1.5/32'::cidr,13)));

-- v6
SELECT set_masklen(cidr '1:1:897d::ddff',88) AS RESULT;
SELECT set_masklen('::/128'::cidr,0) AS RESULT;
SELECT set_masklen(cidr 'FC00::/7',64) AS RESULT;
SELECT set_masklen('::1/128',123) AS RESULT;
SELECT set_masklen('::10.2.3.4',88+20) AS RESULT;
SELECT set_masklen(cidr'::ffff:10.4.3.2/128',5*21) AS RESULT;

-- cidr
SELECT set_masklen('192.168.100.128/25'::cidr,31) AS RESULT;
SELECT set_masklen('192.168/24'::cidr,0) AS RESULT;
SELECT set_masklen('192.168/25'::cidr,7) AS RESULT;
SELECT set_masklen('192.168.1'::cidr,23) AS RESULT;
SELECT set_masklen('192.168'::cidr,32) AS RESULT;
SELECT set_masklen('10.1.2'::cidr,3) AS RESULT;
SELECT set_masklen('10.1'::cidr,32) AS RESULT;
SELECT set_masklen('10'::cidr,5) AS RESULT;
SELECT set_masklen('10.1.2.3/32'::cidr,12) AS RESULT;
SELECT set_masklen('2001:4f8:3:ba::/64'::cidr,123) AS RESULT;
SELECT set_masklen('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr,3) AS RESULT;
SELECT set_masklen('::ffff:1.2.3.0/120'::cidr,123) AS RESULT;
SELECT set_masklen('::ffff:1.2.3.0/128'::cidr,12) AS RESULT;