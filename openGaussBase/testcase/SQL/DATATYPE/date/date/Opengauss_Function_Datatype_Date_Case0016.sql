-- @testpoint: 日期类型相加，合理报错
-- @modified at: 2020-11-18

DROP TABLE IF EXISTS test_date16;
CREATE TABLE test_date16 (name date);
insert into  test_date16 values (DATE '2018-09-17' +  DATE '2018-09-16');
DROP TABLE test_date16;