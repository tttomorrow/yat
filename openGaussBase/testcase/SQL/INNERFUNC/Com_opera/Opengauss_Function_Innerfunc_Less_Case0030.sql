-- @testpoint: opengauss比较操作符<,不支持比较的类型polygon，合理报错
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col polygon, col1 polygon);
INSERT INTO ts_zhparser VALUES(polygon'(1,1),(2,2),(3,3)',polygon'(1,1),(2,2),(4,4)');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;