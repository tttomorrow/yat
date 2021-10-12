-- @testpoint: opengauss逻辑操作符OR,两个null
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, index int);
select id OR index from ts_zhparser;
drop table if exists ts_zhparser;