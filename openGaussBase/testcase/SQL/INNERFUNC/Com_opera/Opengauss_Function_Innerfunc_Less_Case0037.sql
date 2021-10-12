-- @testpoint: opengauss比较操作符<,不支持比较的类型json，合理报错
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col json, col1 json);
INSERT INTO ts_zhparser VALUES('{ "name":"runoob"}','{"name":"runoob", "alexa":10000}');
select col < col1 from ts_zhparser;
drop table if exists ts_zhparser;