-- @testpoint: opengauss比较操作符<,不支持隐式转换的类型做比较，合理报错
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id TINYINT, index json);
INSERT INTO ts_zhparser VALUES(100, '{"f1":1,"f2":true,"f3":"Hi"}');
select * from ts_zhparser where id < index;
drop table if exists ts_zhparser;