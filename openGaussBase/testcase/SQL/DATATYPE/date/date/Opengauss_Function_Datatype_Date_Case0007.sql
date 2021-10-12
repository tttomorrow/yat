-- @testpoint: 日期型数据与数值相减，更新新的日期

DROP TABLE IF EXISTS test_date07;
CREATE TABLE test_date07 (name date);
INSERT INTO test_date07 VALUES ( DATE '2018-09-17'- 1/24);
select * from test_date07;
DROP TABLE test_date07;