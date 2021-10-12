-- @testpoint: 网络地址函数family(inet)异常校验，合理报错

-- v4
SELECT family('0.0.0.0.0') AS RESULT;
SELECT family('255.255.255.256') AS RESULT;
SELECT family('192.168.1.6/33') AS RESULT;
SELECT family('192.168.1.6/255.255.255.255') AS RESULT;

-- v6
SELECT family('::eeff::/128') AS RESULT;
SELECT family('234e:0:4567::3h') AS RESULT;
SELECT family('234e:0:4567::3e/129') AS RESULT;
SELECT family('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff:eedd') AS RESULT;


SELECT family('::ffff:10.4.3.2:1111/64') AS RESULT;
SELECT family('10.2.3.4::1') AS RESULT;

-- 其它
SELECT family('12:34:56:78:90:ab') AS RESULT;
SELECT family('234e::10:4567::3e.ff') AS RESULT;

SELECT family('') AS RESULT;
SELECT family('192.168.1.6/27','192.168.1.6/27') AS RESULT;

-- cidr
SELECT family('192.168.100.128-25'::cidr) AS RESULT;
SELECT family('192.168/25':cidr) AS RESULT;
SELECT family('10'::cidr1) AS RESULT;
SELECT family('2001:4f8:3:ba::/129'::cidr) AS RESULT;
SELECT family('2001:4f8:3:ba:2e0:81ff:fe22:d1gh'::cidr) AS RESULT;