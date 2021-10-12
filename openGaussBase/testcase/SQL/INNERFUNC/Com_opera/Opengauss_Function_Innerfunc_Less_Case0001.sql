-- @testpoint: opengauss比较操作符<,比较类型:TINYINT
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id TINYINT, index TINYINT);
INSERT INTO ts_zhparser VALUES(2, 100);
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;
