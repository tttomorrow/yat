-- @testpoint: 只输入日期，不输入时间

DROP TABLE IF EXISTS test_timestamp12;
CREATE TABLE test_timestamp12 (name TIMESTAMP);
INSERT INTO test_timestamp12 VALUES (TIMESTAMP '2018-09-16');
select * from test_timestamp12;
drop table test_timestamp12;