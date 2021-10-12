-- @testpoint: opengauss比较操作符>=，作为表查询条件
-- 与表查询的联合使用
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id CHAR(5), index NCHAR(5));
INSERT INTO ts_zhparser VALUES('xbc', 'stude');
select * from ts_zhparser where id >= index;
drop table if exists ts_zhparser;