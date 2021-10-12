-- @testpoint: octet_length函数输入值为null,空格，空字符
SELECT octet_length(null);
SELECT octet_length(' ');
SELECT octet_length('');