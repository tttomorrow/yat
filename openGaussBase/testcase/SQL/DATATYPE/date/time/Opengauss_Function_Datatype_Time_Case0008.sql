-- @testpoint: time时间类型与数值相加，更新新的时间

DROP TABLE IF EXISTS test_time08;
CREATE TABLE test_time08 (name time);
INSERT INTO test_time08 VALUES ('11:22:33.456' + interval '3 hours');
select * from test_time08;
DROP TABLE test_time08;