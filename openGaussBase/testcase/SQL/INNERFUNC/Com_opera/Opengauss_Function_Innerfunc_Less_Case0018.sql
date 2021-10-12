-- @testpoint: opengauss比较操作符<,比较类型:blob
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(mon blob, mon1 blob);
INSERT INTO ts_zhparser VALUES('01010', '010101');
select * from ts_zhparser where mon < mon1;
drop table if exists ts_zhparser;