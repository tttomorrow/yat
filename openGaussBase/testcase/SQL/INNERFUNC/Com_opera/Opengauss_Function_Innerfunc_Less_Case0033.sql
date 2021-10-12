-- @testpoint: opengauss比较操作符<,比较类型:macaddr
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col macaddr, col1 macaddr);
INSERT INTO ts_zhparser VALUES('08:00:2b:01:02:03','08:00:2b:01:02:04');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;