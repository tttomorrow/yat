-- @testpoint: opengauss逻辑操作符OR,一个为真一个为null
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, index int);
INSERT INTO ts_zhparser(id) VALUES(2);
select * from ts_zhparser where id >1 OR index;
drop table if exists ts_zhparser;