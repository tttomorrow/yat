-- @testpoint: 日期型数据与数值相加,更新新的日期

DROP TABLE IF EXISTS test_date06;
CREATE TABLE test_date06 (name date);
INSERT INTO test_date06 VALUES (DATE '2018-09-17' + 1);
select * from test_date06;
drop table test_date06;