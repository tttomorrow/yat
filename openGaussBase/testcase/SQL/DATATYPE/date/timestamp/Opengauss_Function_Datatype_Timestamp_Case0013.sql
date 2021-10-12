-- @testpoint: 输入为空值

DROP TABLE IF EXISTS test_timestamp13;
CREATE TABLE test_timestamp13 (id int,name timestamp);
INSERT INTO test_timestamp13 VALUES (1,null);
INSERT INTO test_timestamp13 VALUES (2,'');
SELECT * FROM test_timestamp13;
drop table test_timestamp13;