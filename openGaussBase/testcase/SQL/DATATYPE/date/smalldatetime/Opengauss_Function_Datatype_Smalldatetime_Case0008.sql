-- @testpoint: samlldatetime日期类型与数值相加，更新新的日期

DROP TABLE IF EXISTS test_smalldatetime08;
CREATE TABLE test_smalldatetime08 (name smalldatetime);
INSERT INTO test_smalldatetime08 VALUES (smalldatetime '2018-09-17 11:22:33.456' + 1);
select * from test_smalldatetime08;
DROP TABLE test_smalldatetime08;