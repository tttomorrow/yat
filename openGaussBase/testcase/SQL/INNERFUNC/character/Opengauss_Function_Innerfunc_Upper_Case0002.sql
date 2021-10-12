-- @testpoint: 字母数字特殊字符大小写混写
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('qqAW中国！@￥%');
SELECT upper(string1) from type_char;
DROP TABLE IF EXISTS type_char;