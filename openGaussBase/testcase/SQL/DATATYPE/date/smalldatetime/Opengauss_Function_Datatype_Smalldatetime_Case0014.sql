-- @testpoint: 输入为特殊字符/字母/非隐式字符串，合理报错

DROP TABLE IF EXISTS test_smalldatetime14;
CREATE TABLE test_smalldatetime14 (name smalldatetime);
INSERT INTO test_smalldatetime14 VALUES (smalldatetime 'r');
INSERT INTO test_smalldatetime14 VALUES (smalldatetime '~');
DROP TABLE test_smalldatetime14;