-- @testpoint: opengauss比较操作符<,比较类型:date
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col date, col1 date);
INSERT INTO ts_zhparser VALUES('9999-12-30', '9999-12-31');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;