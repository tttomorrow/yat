--  @testpoint:opengauss关键字INTERVAL 非保留,时间间隔函数
CREATE TABLE day_type_tab (a int,b INTERVAL DAY(3) TO SECOND (4));
INSERT INTO day_type_tab VALUES (1, INTERVAL '3' DAY);
SELECT * FROM day_type_tab;
DROP TABLE day_type_tab;
CREATE TABLE year_type_tab(a int, b interval year (6));
INSERT INTO year_type_tab VALUES(1,interval '2' year);
SELECT * FROM year_type_tab;
DROP TABLE year_type_tab;
SELECT age(timestamp '2001-04-10', timestamp '1957-06-13');

