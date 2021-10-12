-- @testpoint: 结合日期函数，在DATE减少月份得到新日期

DROP TABLE IF EXISTS test_date09;
CREATE TABLE test_date09 (name date);
INSERT INTO test_date09 VALUES (ADD_MONTHS(date '2018-09-18', -1));
SELECT * FROM test_date09;
DROP TABLE test_date09;
