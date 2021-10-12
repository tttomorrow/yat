-- @testpoint: opengauss比较操作符<,比较类型:BOOLEAN
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(mon BOOLEAN, mon1 BOOLEAN);
INSERT INTO ts_zhparser VALUES(false, true);
select * from ts_zhparser where mon < mon1;
drop table if exists ts_zhparser;