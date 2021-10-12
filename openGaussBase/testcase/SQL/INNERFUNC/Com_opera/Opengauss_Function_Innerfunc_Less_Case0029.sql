-- @testpoint: opengauss比较操作符<,不支持比较的类型point，合理报错
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col point, col1 point);
INSERT INTO ts_zhparser VALUES(point'(1,1)',point'(2,2)');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;