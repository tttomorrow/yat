-- @testpoint: 网络地址操作符~(位非)合法值测试


-- v4
SELECT ~ inet '0.0.0.0' AS RESULT;
SELECT ~ inet '127.0.0.1/24' AS RESULT;
SELECT ~ inet '192.168.1.6' AS RESULT;
SELECT ~ inet '255.255.255.255' AS RESULT;
SELECT ~ inet '255.255.255.255/32' AS RESULT;
SELECT ~ cidr '10' AS RESULT;
SELECT ~ cidr '10.1.2.3/32' AS RESULT;

-- v6
SELECT ~ inet '1::1:ddff/64' AS RESULT;
SELECT ~ inet '1:1:897d::ddff' AS RESULT;
SELECT ~ inet '::/128' AS RESULT;
SELECT ~ inet 'FC00::/7' AS RESULT;
SELECT ~ inet '::ffff:10.4.3.2/128' AS RESULT;
SELECT ~ cidr '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128' AS RESULT;

