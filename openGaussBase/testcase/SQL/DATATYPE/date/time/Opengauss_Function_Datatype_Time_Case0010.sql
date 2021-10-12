-- @testpoint: 插入含时区time类型正常值

DROP TABLE IF EXISTS test_time10;
CREATE TABLE test_time10 (name time);
INSERT INTO test_time10 VALUES (time '04:05:06 PST');
INSERT INTO test_time10 VALUES (time '15:05:55 PST');
select * from test_time10;
DROP TABLE IF EXISTS test_time10;