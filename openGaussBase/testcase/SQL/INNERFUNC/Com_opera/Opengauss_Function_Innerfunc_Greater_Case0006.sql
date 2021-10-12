-- @testpoint: opengauss比较操作符>,比较类型:BIGINT
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id BIGINT, index BIGINT);
INSERT INTO ts_zhparser VALUES(7671881, 7671881);
select * from ts_zhparser where id > index;
drop table if exists ts_zhparser;