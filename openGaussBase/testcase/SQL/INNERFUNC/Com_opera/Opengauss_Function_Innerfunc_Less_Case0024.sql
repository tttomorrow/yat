-- @testpoint: opengauss比较操作符<,比较类型:timestamp
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col timestamp, col1 timestamp);
INSERT INTO ts_zhparser VALUES(to_timestamp('0001-01-01 00:00:00.000000','yyyy-mm-dd hh24:mi:ss.ff'), to_timestamp('9999-12-31 23:59:59.999999','yyyy-mm-dd hh24:mi:ss.ff'));
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;