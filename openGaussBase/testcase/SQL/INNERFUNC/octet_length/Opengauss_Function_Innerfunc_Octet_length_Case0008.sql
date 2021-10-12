-- @testpoint: octet_length函数输入值为浮点型
SELECT octet_length(123321.34253);
SELECT octet_length(21.34253);
SELECT octet_length(-1.34253);
SELECT octet_length(0.34253);
