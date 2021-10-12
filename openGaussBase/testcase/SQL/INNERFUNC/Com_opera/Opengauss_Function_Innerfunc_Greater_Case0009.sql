-- @testpoint: opengauss比较操作符>,比较类型:CHAR(n)&NCHAR
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id CHAR(5), index NCHAR(5));
INSERT INTO ts_zhparser VALUES('stude', 'stu');
select * from ts_zhparser where id > index;
drop table if exists ts_zhparser;