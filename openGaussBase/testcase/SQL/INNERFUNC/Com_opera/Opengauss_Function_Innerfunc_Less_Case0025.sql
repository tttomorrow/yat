-- @testpoint: opengauss比较操作符<,比较类型:box
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col box, col1 box);
INSERT INTO ts_zhparser VALUES(box'(1,1),(2,2)',box'(1,1),(2,3)');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;