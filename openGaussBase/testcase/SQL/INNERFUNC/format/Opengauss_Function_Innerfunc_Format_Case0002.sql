-- @testpoint: 格式化字符串:空值,合理报错
SELECT format('Hello %s, %1$s', '');
SELECT format('Hello %s, %1$s', ' ');
SELECT format('Hello %s, %1$s', );
SELECT format('Hello %s, %1$s',null);
SELECT format('Hello %s, %1$s', none);
