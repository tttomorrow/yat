-- @testpoint: 网络地址操作符-的合法值测试

-- 减数字
SELECT inet '255.255.255.250/24' - 5 AS RESULT;
SELECT cidr '10.1.2.3/32' - 25 AS RESULT;
SELECT cidr '2001:4f8:3:ba::/64' - 25 AS RESULT;
SELECT inet '255.255.255.250/24' - -5 AS RESULT;
SELECT inet '255.255.255.250/24' - 999/3 AS RESULT;
SELECT inet '255.255.255.250/24' - 245-5 AS RESULT;
SELECT inet '255.255.255.250/24' - (245-5) AS RESULT;
SELECT inet '255.255.255.255/24' - 429496729 AS RESULT;
SELECT cidr '192.168' - 25 AS RESULT;
SELECT cidr '10.1.2' - 25 AS RESULT;
SELECT cidr '192.168' - 25 AS RESULT;
SELECT inet '255.255.255.255' - 4294967295 AS RESULT;
SELECT inet '234e:0:4567::3f' - 1 AS RESULT;
SELECT inet '::1' - '::2' AS RESULT;
SELECT inet '255.255.255.250' - 0.7 AS RESULT;
SELECT inet '::1/128' - -9.34 AS RESULT;
SELECT inet '1::ffff:255.255.255.250' - 9/9 AS RESULT;
SELECT inet '1::ffff:255.255.250.255' - 9/9 AS RESULT;
SELECT inet '1::ffff:255.255.250.250' - 9/9 AS RESULT;
-- 减ip
SELECT inet '255.255.255.255/24' - cidr '10.1.2' AS RESULT;
SELECT inet '255.255.255.255/24' - cidr '0.0.0.1' AS RESULT;
SELECT inet '192.168.1.43' - inet '192.168.1.19' AS RESULT;
SELECT inet '1::ffff:255.255.250.250' - '1::ffff:255.255.250.229' AS RESULT;
SELECT inet '1::ffff:255.255.250.250' - '1::ffff:255.255.250.249' AS RESULT;
SELECT inet '1::ffff:255.255.255.255' - '1::ffff:0:0' AS RESULT;
SELECT inet '1::ffff:255.255.250.249' - '1::ffff:255.255.250.250' AS RESULT;


SELECT cidr '10.1.2' - '25'::clob AS RESULT;
SELECT cidr '192.168' - 0.025 AS RESULT;






