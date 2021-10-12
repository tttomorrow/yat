-- @testpoint: 网络地址操作符~的异常校验，合理报错

-- v4
SELECT ~ inet '0.0.0.0.0' AS RESULT;
SELECT ~ inet '127.0.0.1/33' AS RESULT;
SELECT ~ inet '256.168.1.6' AS RESULT;
SELECT ~ inet1 '255.255.255.255' AS RESULT;
SELECT ~ cidr '10!' AS RESULT;
SELECT ~ cidr '10.1.2.3@32' AS RESULT;

-- v6
SELECT ~ inet '1::1:ddff/129' AS RESULT;
SELECT ~ inet '1:1:897d::ddfh' AS RESULT;
SELECT ~ inet '1::1::3/128' AS RESULT;
SELECT ~ inet 'FC001::/7' AS RESULT;
SELECT ~ cidr '2001:4f8:3:ba:2e0:81ff:fe22:d1f1:8/128' AS RESULT;

-- 多参少参空值
SELECT ~ cidr ' ' AS RESULT;
SELECT ~ cidr '' AS RESULT;