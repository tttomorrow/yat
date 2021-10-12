-- @testpoint: 结合日期函数，在DATE增加/减少月份得到新日期

DROP TABLE IF EXISTS test_timestamp10;
CREATE TABLE test_timestamp10 (name TIMESTAMP);
INSERT INTO test_timestamp10 VALUES (ADD_MONTHS(TIMESTAMP '2018-09-18 11:22:33.456', +1));
INSERT INTO test_timestamp10 VALUES (ADD_MONTHS(TIMESTAMP '2018-09-18 11:22:33.456', -1));
select * from test_timestamp10;
DROP TABLE IF EXISTS test_timestamp10;