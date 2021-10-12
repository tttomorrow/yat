-- @testpoint: 模式匹配操作符SIMILAR TO,使用下划线_匹配任何单个字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(10));
insert into type_char values ('a_bcd');
SELECT  * from type_char  where string1 SIMILAR TO 'a_bc_';
SELECT  * from type_char  where string1 SIMILAR TO 'a__c_';
SELECT  * from type_char  where string1 SIMILAR TO 'a_bc_';
DROP TABLE IF EXISTS type_char;