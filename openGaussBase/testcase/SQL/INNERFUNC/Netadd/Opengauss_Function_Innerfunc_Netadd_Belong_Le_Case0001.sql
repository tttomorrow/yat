-- @testpoint: 网络地址操作符<<=(包含于或等于)合法值测试

-- 32位掩码属于任何
SELECT inet '127.0.0.1/32' <<= inet '0.0.0.0/1' AS RESULT;
-- 网络号长的属于网络号短的
SELECT inet '192.168.1/24' <<= inet '192.168.1/24' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1.9/0' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1.9/7' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1/23' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1/24' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1/25' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1/29' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1/30' AS RESULT;
SELECT inet '192.168.1.5' <<= inet '192.168.1/31' AS RESULT;

SELECT inet '234e:0:4567::3f' <<= inet '234e:0:4567::3f/128' AS RESULT;
SELECT inet '234e:0:7777::3f' <<= inet '234e:0:4567::3f/2' AS RESULT;
SELECT inet '::ffff:1.2.3.0/128' <<= inet '::aaaa/64' AS RESULT;

SELECT '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr <<= inet '2001::/16' AS RESULT;
SELECT '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr <<= inet '2999::/1' AS RESULT;
-- 不属于
SELECT inet '10.4.3.2' <<= inet '::ffff:10.4.3.2' AS RESULT;
SELECT inet '::ffff:1.2.3.0/128' <<= inet '1.2.3.0' AS RESULT;