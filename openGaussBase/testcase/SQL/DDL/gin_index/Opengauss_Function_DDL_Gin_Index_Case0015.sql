--  @testpoint: create gin index:数据更新后

SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;



--row table
DROP TABLE IF EXISTS test_gin_row1;
CREATE TABLE test_gin_row1 (id INT, info INT[]);

--insert data
INSERT INTO test_gin_row1 SELECT g, ARRAY[1, g % 5, g] FROM generate_series(1, 200000) g;

--create gin index
CREATE INDEX  test_gin_row1_idx ON test_gin_row1 USING GIN(info);

INSERT INTO test_gin_row1 VALUES(200001, array[1,3,5,6,7]);
INSERT INTO test_gin_row1 VALUES(2, array[2,3,5,8,7]);
INSERT INTO test_gin_row1 VALUES(3, array[3,3,5,8,7]);


--query
SELECT * FROM test_gin_row1 WHERE info=array[1,3,5,6,7];
explain SELECT * FROM test_gin_row1 WHERE info=array[1,3,5,6,7];
--update
update test_gin_row1 set info=array[2,3,5,7,7] WHERE id = 200001;
SELECT * FROM test_gin_row1 WHERE info=array[1,3,5,6,7];
explain SELECT * FROM test_gin_row1 WHERE info=array[1,3,5,6,7];
--delete
delete from test_gin_row1 WHERE id = 200001;
SELECT * FROM test_gin_row1 WHERE info=array[2,3,5,7,7];
explain SELECT * FROM test_gin_row1 WHERE info=array[2,3,5,7,7];

--teaeDown drop table
DROP TABLE IF EXISTS test_gin_row2;

