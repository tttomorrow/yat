-- @testpoint: 插入空值

DROP TABLE IF EXISTS test_date15;
CREATE TABLE test_date15 (id int,name date);
INSERT INTO test_date15 VALUES (1,null);
INSERT INTO test_date15 VALUES (2,'');
select * from test_date15;
DROP TABLE test_date15;