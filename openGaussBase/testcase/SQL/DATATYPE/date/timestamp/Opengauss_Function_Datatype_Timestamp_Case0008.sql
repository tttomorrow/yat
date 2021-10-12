-- @testpoint: timestamp日期类型与数值相加更新新的日期

DROP TABLE IF EXISTS test_timestamp08;
CREATE TABLE test_timestamp08 (name TIMESTAMP);
INSERT INTO test_timestamp08 VALUES (timestamp '2018-09-17 11:22:33.456'+ 1);
select * from test_timestamp08;
DROP TABLE IF EXISTS test_timestamp08;