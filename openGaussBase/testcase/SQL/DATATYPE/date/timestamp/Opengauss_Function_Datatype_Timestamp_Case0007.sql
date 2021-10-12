-- @testpoint: 输入字符串型日期，类型前加timestamp进行转换

DROP TABLE IF EXISTS test_timestamp07;
CREATE TABLE test_timestamp07 (A INT,B timestamp);
INSERT INTO test_timestamp07 VALUES (1,timestamp '2018-09-16 11:22:33.456');
INSERT INTO test_timestamp07 VALUES (2,timestamp '2018-09-17 11:22:33.456');
SELECT * FROM test_timestamp07;
drop table test_timestamp07;