-- @testpoint: 网络地址操作符>>=(包含)合法值测试

-- 0为掩码包含所有
SELECT inet '192.168.1/0' >>= inet '192.168.1.5' AS RESULT;
SELECT inet '192.168.1/0' >>= inet '255.255.255.255' AS RESULT;
SELECT inet '0.0.0.0/0' >>= inet '127.0.0.1/24' AS RESULT;
-- 同网段短掩码包含长掩码的
SELECT inet '192.168.1/2' >>= inet '192.168.1/24' AS RESULT;
SELECT inet '192.168.1.5/7' >>= inet '192.168.1.9' AS RESULT;
SELECT inet '192.168.1.5/23' >>= inet '192.168.1.9' AS RESULT;
SELECT inet '192.168.1.5/25' >>= inet '192.168.1.2' AS RESULT;
SELECT inet '192.168.1.128/29' >>= inet '192.168.1.8' AS RESULT;
-- 网络号同，主机位小的包含主机位大的
SELECT inet '192.168.1/24' >>= inet '192.168.1/24' AS RESULT;
SELECT inet '192.168.1/24' >>= inet '192.168.1.9/24' AS RESULT;
SELECT inet '1.1.1/8' >>= inet '1.2.3.4/8' AS RESULT;

SELECT inet '234e:0:4567::3f/127' >>= inet '234e:0:4567::3f/128' AS RESULT;
SELECT inet '234e:0:4567::3f/2' >>= inet '234e:0:7777::3f' AS RESULT;
SELECT inet '::aaaa/64' >>= inet '::ffff:1.2.3.0/128' AS RESULT;

SELECT '2001::/16'::cidr >>= inet '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128' AS RESULT;
SELECT '2::/1'::inet >>= inet '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/124' AS RESULT;

-- 根本不包含的
SELECT inet '10.4.3.2' >>= inet '::ffff:10.4.3.2' AS RESULT;
SELECT inet '::ffff:1.2.3.0/128' >>= inet '1.2.3.0' AS RESULT;