-- @testpoint: 网络地址函数family(inet)抽取地址族

-- v4
SELECT family('0.0.0.0') AS RESULT;
SELECT family('127.0.0.1') AS RESULT;
SELECT family('255.255.255.255') AS RESULT;
SELECT family('192.168.1.6/27') AS RESULT;

-- v6
SELECT family('::/128') AS RESULT;
SELECT family('234e:0:4567::3e') AS RESULT;
SELECT family('234e:0:4567::3e/127') AS RESULT;
SELECT family('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff') AS RESULT;


SELECT family('::ffff:10.4.3.2') AS RESULT;
SELECT family('::10.2.3.4') AS RESULT;
SELECT family('1::ffff:10.4.3.2/24') AS RESULT;

-- cidr
SELECT family('192.168.100.128/25'::cidr) AS RESULT;
SELECT family('192.168/24'::cidr) AS RESULT;
SELECT family('192.168/25'::cidr) AS RESULT;
SELECT family('192.168.1'::cidr) AS RESULT;
SELECT family('192.168'::cidr) AS RESULT;
SELECT family('10.1.2'::cidr) AS RESULT;
SELECT family('10.1'::cidr) AS RESULT;
SELECT family('10'::cidr) AS RESULT;
SELECT family('10.1.2.3/32'::cidr) AS RESULT;
SELECT family('2001:4f8:3:ba::/64'::cidr) AS RESULT;
SELECT family('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr) AS RESULT;
SELECT family('::ffff:1.2.3.0/120'::cidr) AS RESULT;
SELECT family('::ffff:1.2.3.0/128'::cidr) AS RESULT;