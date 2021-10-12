-- @testpoint: 结合where条件语句

DROP TABLE IF EXISTS test_time06;
CREATE TABLE test_time06 (A INT,B time);
INSERT INTO test_time06 VALUES (1,'11:22:33.456');
INSERT INTO test_time06 VALUES (2,'23:45:56.789');
SELECT A,B FROM test_time06 where B = '11:22:33.456' order by A;
drop table test_time06;