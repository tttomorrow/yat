-- @testpoint: opengauss逻辑操作符AND,运算交换性验证
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, index int);
INSERT INTO ts_zhparser VALUES(2, 100);
select * from ts_zhparser where id >1 AND index >50;
select * from ts_zhparser where index >50 AND id >1;
drop table if exists ts_zhparser;