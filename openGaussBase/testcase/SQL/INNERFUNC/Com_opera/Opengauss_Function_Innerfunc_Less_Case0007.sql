-- @testpoint: opengauss比较操作符<,比较类型:char
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id CHAR(5), index CHAR(5));
INSERT INTO ts_zhparser VALUES('stu', 'stude');
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;