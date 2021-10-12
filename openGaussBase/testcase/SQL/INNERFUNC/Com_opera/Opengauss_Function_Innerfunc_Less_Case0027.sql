-- @testpoint: opengauss比较操作符<,比较类型:lseg
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col lseg, col1 lseg);
INSERT INTO ts_zhparser VALUES(lseg'(1,1),(2,2)',lseg'(1,1),(2,3)');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;