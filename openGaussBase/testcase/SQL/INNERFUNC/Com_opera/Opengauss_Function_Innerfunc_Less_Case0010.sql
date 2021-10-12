-- @testpoint: opengauss比较操作符<,比较类型:VARCHAR
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id VARCHAR(5), index VARCHAR(5));
INSERT INTO ts_zhparser VALUES('stu', 'stude');
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;