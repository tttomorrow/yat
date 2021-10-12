-- @testpoint: opengauss比较操作符<,比较类型:smalldatetime
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col smalldatetime, col1 smalldatetime);
INSERT INTO ts_zhparser VALUES('0001-01-01 00:00:00.000000', '9999-12-31 23:59:59.999999');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;