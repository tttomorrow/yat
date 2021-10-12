-- @testpoint: 结合日期函数，在DATE增加月份得到新日期

DROP TABLE IF EXISTS test_date08;
CREATE TABLE test_date08 (name date);
INSERT INTO test_date08 VALUES (ADD_MONTHS(date '2018-09-18', +1));
INSERT INTO test_date08 VALUES (ADD_MONTHS(date '2018-09-11', -1));
SELECT * FROM test_date08;
DROP TABLE test_date08;
