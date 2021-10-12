-- @testpoint: 结合时间日期函数，在DATE增加/减少月份更新新的日期

DROP TABLE IF EXISTS test_smalldatetime10;
CREATE TABLE test_smalldatetime10 (name smalldatetime);
INSERT INTO test_smalldatetime10 VALUES (ADD_MONTHS(smalldatetime '2018-09-18 11:22:33.456', +1));
INSERT INTO test_smalldatetime10 VALUES (ADD_MONTHS(smalldatetime '2018-09-18 11:22:33.456', -1));
select * from test_smalldatetime10;
DROP TABLE test_smalldatetime10;