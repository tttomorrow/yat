-- @testpoint: 输入字符串型日期，类型前加smalldatetime进行转换

DROP TABLE IF EXISTS test_smalldatetime07;
CREATE TABLE test_smalldatetime07 (A INT,B smalldatetime);
INSERT INTO test_smalldatetime07 VALUES (1,smalldatetime '2018-09-16 11:22:33.456');
INSERT INTO test_smalldatetime07 VALUES (2,smalldatetime '2018-09-17 11:22:33.456');
SELECT * FROM test_smalldatetime07;
drop table test_smalldatetime07;
