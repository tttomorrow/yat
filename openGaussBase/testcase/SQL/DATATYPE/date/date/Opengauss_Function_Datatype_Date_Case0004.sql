-- @testpoint: 结合where条件

DROP TABLE IF EXISTS test_date04;
CREATE TABLE test_date04 (A INT,B DATE);
INSERT INTO test_date04 VALUES (1,DATE '2018-09-16');
INSERT INTO test_date04 VALUES (2,DATE '2018-09-17');
SELECT A,B FROM test_date04 where B = DATE '2018-09-17' order by A;
drop table test_date04;
