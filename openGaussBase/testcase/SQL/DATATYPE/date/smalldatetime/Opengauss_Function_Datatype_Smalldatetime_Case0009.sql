-- @testpoint: samlldatetime日期类型与数值相减，更新新的时间

DROP TABLE IF EXISTS test_date09;
CREATE TABLE test_date09 (name smalldatetime);
INSERT INTO test_date09 VALUES (smalldatetime '2018-09-17 11:22:33.456'- 1/24);
select * from test_date09;
DROP TABLE test_date09;
