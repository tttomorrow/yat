-- @testpoint: 模式匹配操作符LIKE,对%进行匹配，使用escape指定前导逃逸字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('ab%c');
SELECT * from type_char  where string1 LIKE 'ab#%c' escape '#';
DROP TABLE IF EXISTS type_char;