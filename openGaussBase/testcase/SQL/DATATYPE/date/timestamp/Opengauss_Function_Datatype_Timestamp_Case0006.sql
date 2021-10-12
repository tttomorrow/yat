-- @testpoint: 结合where条件语句

DROP TABLE IF EXISTS test_timestamp06;
CREATE TABLE test_timestamp06 (A INT,B TIMESTAMP);
INSERT INTO test_timestamp06 VALUES (1,'2018-09-16 11:22:33.456');
INSERT INTO test_timestamp06 VALUES (2,'2018-09-17 11:22:33.456');
SELECT A,B FROM test_timestamp06 where B = '2018-09-17 11:22:33.456' order by A;
drop table test_timestamp06;