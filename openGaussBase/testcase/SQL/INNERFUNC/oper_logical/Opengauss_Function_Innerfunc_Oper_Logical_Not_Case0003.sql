-- @testpoint: opengauss逻辑操作符NOT, null
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, stu CHAR(5));
INSERT INTO ts_zhparser VALUES(2, 'stude');
select * from ts_zhparser where id  is  NOT null ;
drop table if exists ts_zhparser;