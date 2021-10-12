-- @testpoint: opengauss逻辑操作符NOT,与其它逻辑操作符连用
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(id int, stu int);
INSERT INTO ts_zhparser VALUES(2, 100);
select * from ts_zhparser where stu >50 AND id  is  NOT null ;
drop table if exists ts_zhparser;