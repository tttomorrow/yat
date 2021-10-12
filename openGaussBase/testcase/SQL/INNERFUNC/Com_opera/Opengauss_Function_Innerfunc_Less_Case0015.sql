-- @testpoint: opengauss比较操作符<,比较类型:money
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(mon money, mon1 money);
INSERT INTO ts_zhparser VALUES(2, 100);
select * from ts_zhparser where mon < mon1;
drop table if exists ts_zhparser;