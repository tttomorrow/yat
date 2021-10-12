-- @testpoint: timestamp日期类型与数值相减更新新的日期

DROP TABLE IF EXISTS test_date09;
CREATE TABLE test_date09 (name TIMESTAMP);
INSERT INTO test_date09 VALUES (TIMESTAMP '2018-09-17 11:22:33.456'- 1);
select * from test_date09;
DROP TABLE IF EXISTS test_date09;
