-- @testpoint: 字符本身含有_
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('AA_BBCC');
SELECT  (string1 LIKE '%A@_B%' ESCAPE '@') from type_char AS RESULT;
DROP TABLE IF EXISTS type_char;