-- @testpoint: 网络地址操作符=(等于)异常校验，合理报错


SELECT inet '8.256.1.5' = inet '8.256.1.4' AS RESULT;
SELECT inet '8.168.1.4' = inet '8.168.1.4/33' AS RESULT;

SELECT inet '234e:0:4567::3f/129' = inet '234e:0:4567::3f/127' AS RESULT;
SELECT inet '::aaas:192.168.1.5' = inet '192.168.1.4' AS RESULT;
SELECT inet '::aaaaa:192.168.1.5/112' = inet '::aaa:192.168.1.4/112' AS RESULT;
SELECT  cidr '1::1 /32' = cidr '1::1 /32' AS RESULT;


SELECT '121.168.1.5'::inet = ''::inet AS RESULT;
SELECT ''::inet = ''::inet AS RESULT;

SELECT inet '192.168.1.5' = inet '192.168.1.4' = inet '192.168.1.4'AS RESULT;

SELECT  '@' = inet '@' AS RESULT;
SELECT  '1::1 /8' =  '1::1 /8' =  '1::1 /8' AS RESULT;