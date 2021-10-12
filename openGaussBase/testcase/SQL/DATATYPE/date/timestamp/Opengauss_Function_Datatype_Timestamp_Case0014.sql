-- @testpoint: 输入为特殊字符，合理报错

DROP TABLE IF EXISTS test_timestamp14;
CREATE TABLE test_timestamp14 (name timestamp);
INSERT INTO test_timestamp14 VALUES (timestamp 'r');
INSERT INTO test_timestamp14 VALUES (timestamp '~');
DROP TABLE IF EXISTS test_timestamp14;