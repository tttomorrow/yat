-- @testpoint: opengauss逻辑操作符AND,一个为假一个为null
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, index int);
INSERT INTO ts_zhparser(id) VALUES(2);
select id >2 AND NULL FROM ts_zhparser; 
drop table if exists ts_zhparser;