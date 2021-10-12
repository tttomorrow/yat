-- @testpoint: opengauss比较操作符<,比较类型:inet
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col inet, col1 inet);
INSERT INTO ts_zhparser VALUES('192.168.31/24','192.168.31.32/24');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;