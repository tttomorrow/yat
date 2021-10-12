-- @testpoint: opengauss比较操作符<,比较类型:INTEGER
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id INTEGER, index INTEGER);
INSERT INTO ts_zhparser VALUES(2, 7671);
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;