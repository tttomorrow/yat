-- @testpoint: opengauss比较操作符<,可以隐式转换的不同类型
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id TINYINT, index char(5));
INSERT INTO ts_zhparser VALUES(100, 'a');
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;