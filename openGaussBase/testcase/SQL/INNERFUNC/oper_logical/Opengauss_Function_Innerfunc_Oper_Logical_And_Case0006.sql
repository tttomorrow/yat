-- @testpoint: opengauss逻辑操作符AND,三个都为true
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, index int);
INSERT INTO ts_zhparser VALUES(2, 100);
select * from ts_zhparser where id >1 AND index >50 AND index<120;
drop table if exists ts_zhparser;