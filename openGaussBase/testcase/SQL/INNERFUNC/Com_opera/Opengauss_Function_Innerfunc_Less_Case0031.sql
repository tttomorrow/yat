-- @testpoint: opengauss比较操作符<,比较类型:cidr
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col cidr, col1 cidr);
INSERT INTO ts_zhparser VALUES('192.168.31/24','192.168.100.128/25');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;