-- @testpoint: 插入空值

DROP TABLE IF EXISTS test_time13;
CREATE TABLE test_time13 (id int,name time);
INSERT INTO test_time13 VALUES (1,null);
INSERT INTO test_time13 VALUES (2,'');
SELECT * FROM test_time13;
drop table test_time13;