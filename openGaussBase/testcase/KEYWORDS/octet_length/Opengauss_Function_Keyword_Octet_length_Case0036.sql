-- @testpoint: opengauss关键字octet_length(非保留)，统计字符串中的字节数
SELECT octet_length('jose');
SELECT octet_length('你好');
SELECT octet_length('你好@123');
SELECT octet_length('');
