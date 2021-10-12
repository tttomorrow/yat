-- @testpoint: opengauss比较操作符<,比较类型:INTEGER&BINARY_INTEGER
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id INTEGER, index BINARY_INTEGER);
INSERT INTO ts_zhparser VALUES(2, 767188);
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;