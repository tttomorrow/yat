-- @testpoint: opengauss逻辑操作符NOT,为真
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, stu CHAR(5));
INSERT INTO ts_zhparser VALUES(2, 'stude');
select 'q' NOT in (select stu from ts_zhparser );
drop table if exists ts_zhparser;