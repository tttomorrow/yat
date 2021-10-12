-- @testpoint: 中文字母数字特殊字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abcdeF1中国@#￥');
SELECT repeat(string1,4) from type_char;
DROP TABLE IF EXISTS type_char;