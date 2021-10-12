-- @testpoint: opengauss比较操作符<,连比，合理报错
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id TINYINT, index TINYINT,clo TINYINT);
INSERT INTO ts_zhparser VALUES(10,1,3);
select * from ts_zhparser where id < index < clo;
drop table if exists ts_zhparser;