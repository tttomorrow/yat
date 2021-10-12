-- @testpoint: opengauss比较操作符<,比较类型:bit varying
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col bit varying, col1 bit varying);
INSERT INTO ts_zhparser VALUES(B'10001',B'11011');
select col < col1 from ts_zhparser;
drop table if exists ts_zhparser;