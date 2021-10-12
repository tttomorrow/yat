-- @testpoint: 网络地址操作符<>(不等于)合法值测试

 -- A&A
SELECT inet '8.168.1.5' <> inet '8.168.1.4' AS RESULT;
SELECT inet '8.168.1.4' <> inet '8.168.1.4/24' AS RESULT;
 -- B&C
SELECT inet '121.168.1.5' <> inet '192.168.1.4' AS RESULT;
 -- C&C
SELECT inet '192.168.1.5' <> inet '192.168.1.4' AS RESULT;
SELECT inet '192.168.1.5/8' <> inet '192.168.1.4/8' AS RESULT;
SELECT inet '192.168.1.8/16' <> inet '192.168.1.8/24' AS RESULT;
 -- 6&6
 SELECT inet '234e:0:4567::3f/128' <> inet '234e:0:4567::3f/127' AS RESULT;
 -- 6&4
SELECT inet '::aaa:192.168.1.5' <> inet '192.168.1.4' AS RESULT;
SELECT inet '::aaa:192.168.1.5/112' <> inet '::aaa:192.168.1.4/112' AS RESULT;
SELECT  '::1 /32' <>  '::1 /33' AS RESULT;
SELECT  '1::1 /32' <>  '1::1 /32' AS RESULT;
