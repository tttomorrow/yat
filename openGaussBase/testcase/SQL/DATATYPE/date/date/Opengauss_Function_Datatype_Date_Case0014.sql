-- @testpoint: 输入为特殊字符/字母/非隐式字符串，合理报错

DROP TABLE IF EXISTS test_date14;
CREATE TABLE test_date14 (name date);
INSERT INTO test_date14 VALUES (date 'r');
INSERT INTO test_date14 VALUES (date '~');
select * from test_date14;
DROP TABLE test_date14;