-- @testpoint: 网络地址操作符<<(包含于)异常校验，合理报错

SELECT inet '192.168.1.256/16' << inet '192.168.1.8/24' AS RESULT;
SELECT inet '192.168.1.8/16' << inet '192.168.1.8.1/16' AS RESULT;
SELECT inet '192.168.1.8/33' << inet '192.168.1.8/16' AS RESULT;

SELECT inet '234e:0:4567::3f/1' << inet '234e::4567::3f/0' AS RESULT;
SELECT inet '234e:0:45677::3f/127' << inet '234e:0:4567::3f/128' AS RESULT;
SELECT inet '234e:0:4567::3f/129' << inet '234e:0:4567::3f/128' AS RESULT;
SELECT inet '8.168.1.3/24' << inet '8.168.1.3/32' << inet '8.168.1.4' AS RESULT;

SELECT inet '8.168.1.3/24' << inet '' AS RESULT;
SELECT inet '' << inet '' AS RESULT;

