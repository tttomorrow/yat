-- @testpoint: 被搜索字符最后几位中间用其他隔开
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('trimxx1xx');
SELECT rtrim(string1,'x') from type_char;
DROP TABLE IF EXISTS type_char;