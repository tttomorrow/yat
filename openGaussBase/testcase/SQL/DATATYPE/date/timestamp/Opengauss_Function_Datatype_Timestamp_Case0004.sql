-- @testpoint: timestamp日期类型相减，合理报错

DROP TABLE IF EXISTS test_timestamp04;
CREATE TABLE test_timestamp04 (name timestamp);
insert into  test_timestamp04 values (timestamp '2018-09-17' -  timestamp '2018-09-16');
DROP TABLE IF EXISTS test_timestamp04;
