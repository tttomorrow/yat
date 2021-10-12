-- @testpoint: 不包含_或者%
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(7));
insert into type_char values ('AA_BBCC');
SELECT  (string1 LIKE 'AA_BBCC') from type_char AS RESULT;
DROP TABLE IF EXISTS type_char;