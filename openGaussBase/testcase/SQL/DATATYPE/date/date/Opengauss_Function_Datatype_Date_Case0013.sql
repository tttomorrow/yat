-- @testpoint: 输入字符串型日期，类型前加date进行转换

DROP TABLE IF EXISTS test_date13;
CREATE TABLE test_date13 (A INT,B DATE);
INSERT INTO test_date13 VALUES (1,DATE '2018-09-16');
INSERT INTO test_date13 VALUES (2,DATE '2018-09-17');
SELECT A,B FROM test_date13 ORDER BY A;
drop table test_date13;