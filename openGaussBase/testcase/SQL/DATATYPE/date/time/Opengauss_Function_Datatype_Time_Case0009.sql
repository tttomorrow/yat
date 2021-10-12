-- @testpoint: time时间类型与数值相减，更新新的时间

DROP TABLE IF EXISTS test_time09;
CREATE TABLE test_time09 (name time);
INSERT INTO test_time09 VALUES ('11:22:33.456'- interval '2 hours');
select * from test_time09;
DROP TABLE test_time09;
