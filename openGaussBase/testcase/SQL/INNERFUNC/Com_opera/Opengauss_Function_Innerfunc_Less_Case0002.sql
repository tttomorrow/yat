-- @testpoint: opengauss比较操作符<,比较类型:TINYINT&SMALLINT
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id TINYINT, index SMALLINT);
INSERT INTO ts_zhparser VALUES(2, 767);
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;
