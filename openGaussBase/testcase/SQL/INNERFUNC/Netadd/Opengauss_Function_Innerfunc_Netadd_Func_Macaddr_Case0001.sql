-- @testpoint: 网络地址函数trunc(macaddr)将MAC地址的最后三个字节设置为零。

-- 合法6种格式
SELECT trunc(macaddr '08:00:2b:01:02:03') AS RESULT;
SELECT trunc(macaddr '08-00-2b-01-02-03') AS RESULT;
SELECT trunc(macaddr '08002b:010203') AS RESULT;
SELECT trunc(macaddr '0800.2b01.0203') AS RESULT;
SELECT trunc(macaddr '08002b-010203') AS RESULT;
SELECT trunc(macaddr '08002b010203') AS RESULT;
-- 特殊
SELECT trunc(macaddr 'ffffff-ffffff') AS RESULT;
SELECT trunc(macaddr '000000-000000') AS RESULT;
SELECT trunc(macaddr '111111-111111') AS RESULT;


