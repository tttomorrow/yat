-- @testpoint: 网络地址函数trunc(macaddr)异常校验，合理报错


-- .-:穿插使用
SELECT trunc(macaddr '08:00:2b-01:02-03') AS RESULT;
SELECT trunc(macaddr '08-00.2b-01-02-03') AS RESULT;

--给f以外的字母
SELECT trunc(macaddr '08002y:010203') AS RESULT;

-- 特殊字符等
SELECT trunc(macaddr '0800$2b01$0203') AS RESULT;

-- :或-之间超过2字节
SELECT trunc(macaddr '080:02b0:10203') AS RESULT;

-- 超过48bits
SELECT trunc(macaddr '08-10-10-2b-01-02-03') AS RESULT;

-- 空值
SELECT trunc(macaddr '') AS RESULT;
SELECT trunc() AS RESULT;
SELECT trunc(mac '08:00:2b:01:02:03') AS RESULT;
SELECT trunc(macaddr '08:00:2b-01:02-03','08:00:2b-01:02-03') AS RESULT;
