-- @testpoint: 网络地址操作符&将两个网络地址的每一位都进行“与”操作。

-- A&B
SELECT cidr '10.1.2.3/32' & inet '111.0.0.1' AS RESULT;
SELECT inet '10.1.2.3/32' & inet '127.0.0.1' AS RESULT;
-- B&C
SELECT cidr '127' & cidr '192.168.1.6' AS RESULT;
-- A&C
SELECT inet '192.168.1.6' & inet '10.0.0.0' AS RESULT;
-- A&A
SELECT cidr '10' & cidr '11.10.0.10' AS RESULT;
-- C&C
SELECT inet '192.168.1.6' & inet '192.0.0.7' AS RESULT;
-- 6&6
SELECT cidr '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128' & inet '1::1:ddff/64' AS RESULT;
SELECT inet '::ffff:10.4.3.2/128' & inet '::2/128' AS RESULT;
SELECT inet '::ffff:10.4.3.2/128' & inet '::aaaa:11.7.3.6/64' AS RESULT;
SELECT inet '::127.5.5.5' & inet '::aaaa:11.7.3.6/64' AS RESULT;

-- 连续
SELECT inet '1.1.1.1' & inet '3.3.3.3' & '255.255.255.254'AS RESULT;
-- 混合
SELECT (SELECT ~ inet '192.168.1.6' AS RESULT) & '192.0.0.7'AS RESULT;
SELECT (SELECT ~ inet '192.168.1.6' AS RESULT) & (SELECT ~ inet '0.0.0.2' AS RESULT) AS RESULT;
SELECT ~ ((~ inet '192.168.1.6') & ( ~ ~ inet '0.0.0.2' )) AS RESULT;
