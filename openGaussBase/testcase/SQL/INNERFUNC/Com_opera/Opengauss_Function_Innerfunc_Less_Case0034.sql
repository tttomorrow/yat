-- @testpoint: opengauss比较操作符<,比较类型:bit
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col bit(5), col1 bit(5));
INSERT INTO ts_zhparser VALUES(B'10001',B'11011');
select col < col1 from ts_zhparser;
drop table if exists ts_zhparser;