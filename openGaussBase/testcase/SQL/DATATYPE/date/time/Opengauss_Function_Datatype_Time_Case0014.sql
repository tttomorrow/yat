-- @testpoint: 插入特殊字符，合理报错

DROP TABLE IF EXISTS test_time14;
CREATE TABLE test_time14 (name time);
INSERT INTO test_time14 VALUES (time 'r');
INSERT INTO test_time14 VALUES (time '~');
DROP TABLE test_time14;