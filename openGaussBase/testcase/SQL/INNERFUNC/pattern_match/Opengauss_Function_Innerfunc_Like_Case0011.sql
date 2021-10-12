-- @testpoint: 模式匹配操作符LIKE,要匹配逃逸字符本身，写两个逃逸字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('ab%abeefg');
SELECT * from type_char  where string1 like 'ab%%';
DROP TABLE IF EXISTS type_char;