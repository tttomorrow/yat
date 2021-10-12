-- @testpoint: 输入为空值

DROP TABLE IF EXISTS test_smalldatetime13;
CREATE TABLE test_smalldatetime13 (id int,name smalldatetime);
INSERT INTO test_smalldatetime13 VALUES (1,null);
INSERT INTO test_smalldatetime13 VALUES (2,'');
SELECT * FROM test_smalldatetime13;
drop table test_smalldatetime13;