-- @testpoint: opengauss比较操作符<,比较类型:circle
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col circle, col1 circle);
INSERT INTO ts_zhparser VALUES(circle'<(1,1),2>',circle'<(3,3),3>');
select * from ts_zhparser where col < col1;
drop table if exists ts_zhparser;