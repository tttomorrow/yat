-- @testpoint: opengauss比较操作符>,比较类型:text
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id TEXT, index TEXT);
INSERT INTO ts_zhparser VALUES('stude', 'stude');
select * from ts_zhparser where id > index;
drop table if exists ts_zhparser;