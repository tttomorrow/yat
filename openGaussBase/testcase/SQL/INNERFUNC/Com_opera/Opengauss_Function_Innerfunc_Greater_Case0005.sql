-- @testpoint: opengauss比较操作符>,比较类型:INTEGER&BIGINT
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id INTEGER, index BIGINT);
INSERT INTO ts_zhparser VALUES(76112, 76);
select * from ts_zhparser where id > index;
drop table if exists ts_zhparser;