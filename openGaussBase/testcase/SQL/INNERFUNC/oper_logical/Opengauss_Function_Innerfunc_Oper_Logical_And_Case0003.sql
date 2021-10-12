-- @testpoint: opengauss逻辑操作符AND,一个为真一个为null
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, index int);
INSERT INTO ts_zhparser(id) VALUES(2);
select id >1 AND index from ts_zhparser; 
drop table if exists ts_zhparser;