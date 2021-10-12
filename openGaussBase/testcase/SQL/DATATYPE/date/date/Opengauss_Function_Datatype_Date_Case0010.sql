-- @testpoint: 日期类型有效值测试

DROP TABLE IF EXISTS test_date10;
CREATE TABLE test_date10 (A INT,B date);
INSERT INTO test_date10 VALUES (1,'2018-09-13');
INSERT INTO test_date10 VALUES (2,'2018-09-17');
SELECT * FROM test_date10;
DROP TABLE test_date10;