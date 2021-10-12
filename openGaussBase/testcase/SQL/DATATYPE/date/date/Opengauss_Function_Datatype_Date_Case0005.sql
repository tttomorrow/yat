-- @testpoint: 输入日期类型字符,合理报错
-- @modified at: 2020-11-18

DROP TABLE IF EXISTS test_date05;
CREATE TABLE test_date05 (A INT,B date);
INSERT INTO test_date05 VALUES (1,2018-09-16);
SELECT *  FROM test_date05;
drop table test_date05;