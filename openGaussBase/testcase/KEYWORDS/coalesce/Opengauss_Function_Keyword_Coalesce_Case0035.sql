--  @testpoint:opengauss关键字coalesce(非保留)，表达式函数,返回它的第一个非NULL的参数值。如果参数都为NULL，则返回NULL

CREATE TABLE c_tabl(description varchar(10), short_description varchar(10), last_value varchar(10));
INSERT INTO c_tabl VALUES('abc', 'efg', '123');
INSERT INTO c_tabl VALUES(NULL, 'efg', '123');
INSERT INTO c_tabl VALUES(NULL, NULL, '123');
INSERT INTO c_tabl VALUES(NULL, NULL, NULL);
SELECT description, short_description, last_value, COALESCE(description, short_description, last_value) FROM c_tabl ORDER BY 1, 2, 3, 4;

--清理环境
drop table c_tabl;

--条件表达式函数,返回它的第一个非NULL的参数值。如果参数都为NULL，则返回NULL
SELECT coalesce(NULL,'hello');
SELECT coalesce('hello',NULL);
SELECT coalesce(NULL,NULL);

