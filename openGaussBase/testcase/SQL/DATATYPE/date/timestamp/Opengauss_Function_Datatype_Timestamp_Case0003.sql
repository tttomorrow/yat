-- @testpoint: timestamp日期类型相加，合理报错

DROP TABLE IF EXISTS test_timestamp03;
CREATE TABLE test_timestamp03 (name timestamp);
insert into  test_timestamp03 values (timestamp '2018-09-17' +  timestamp '2018-09-16');
DROP TABLE IF EXISTS test_timestamp03;