-- @testpoint: 网络地址操作符<<(包含于)合法值测试
SELECT inet '192.168.1.5' << inet '192.168.1.9/0' AS RESULT;
SELECT inet '192.168.1.5' << inet '192.168.1.9/7' AS RESULT;
SELECT inet '192.168.1.5' << inet '192.168.1/23' AS RESULT;
SELECT inet '192.168.1.5' << inet '192.168.1/24' AS RESULT;
SELECT inet '192.168.1.5' << inet '192.168.1/25' AS RESULT;
SELECT inet '192.168.1.5' << inet '192.168.1/30' AS RESULT;
SELECT inet '192.168.1.5' << inet '192.168.1/31' AS RESULT;
SELECT inet '234e:0:4567::3f' << inet '234e:0:4567::3f/127' AS RESULT;
SELECT inet '234e:0:7777::3f' << inet '234e:0:4567::3f/12' AS RESULT;
SELECT inet '::ffff:1.2.3.0/128' << inet '::aaaa/64' AS RESULT;
SELECT inet '1.2.3.0' << inet '::ffff:1.2.3.0/128' AS RESULT;
SELECT '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr << inet '2001::/16' AS RESULT;
SELECT '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr << inet '2999::/1' AS RESULT;
SELECT inet '10.4.3.2' << inet '::ffff:10.4.3.2' AS RESULT;
