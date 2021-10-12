-- @testpoint: opengauss比较操作符<,比较类型:RAW
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(mon RAW, mon1 RAW);
INSERT INTO ts_zhparser VALUES('DEADBEE', 'DEADBEEF');
select * from ts_zhparser where mon < mon1;
drop table if exists ts_zhparser;