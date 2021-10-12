--  @testpoint: create gin index:分区表数据插入后创建gin索引，数据类型为tevevtor以及数组
SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;


--partition table
DROP TABLE IF EXISTS test_gin_student_column;
CREATE TABLE test_gin_student_column
(
    num int,
    data1 text,
    data2 text
) WITH (ORIENTATION = COLUMN)
PARTITION BY RANGE(num)
(
    PARTITION num1 VALUES LESS THAN(10000),
    PARTITION num2 VALUES LESS THAN(20000),
    PARTITION num3 VALUES LESS THAN(300000)
);

DROP TABLE IF EXISTS test_gin_student_row;
CREATE TABLE test_gin_student_row
(
    num int,
    data1 text,
    data2 text
    
)
PARTITION BY RANGE(num)
(
    PARTITION num1 VALUES LESS THAN(10000),
    PARTITION num2 VALUES LESS THAN(20000),
    PARTITION num3 VALUES LESS THAN(300000)
);
DROP TABLE IF EXISTS test_gin_student_row2;
CREATE TABLE test_gin_student_row2 (id INT, info INT[])
PARTITION BY RANGE(id)
(
    PARTITION num1 VALUES LESS THAN(10000),
    PARTITION num2 VALUES LESS THAN(20000),
    PARTITION num3 VALUES LESS THAN(300000)
);
--insert data

INSERT INTO test_gin_student_column SELECT num, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;
INSERT INTO test_gin_student_row SELECT num, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;
INSERT INTO test_gin_student_row2 SELECT g, ARRAY[1, g % 5, g] FROM generate_series(1, 200000) g;

--create gin index
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_column1 ON test_gin_student_column USING GIN(to_tsvector('english', data1)) LOCAL;
--refer to special partition
CREATE INDEX test_gin_student_index_column2 ON test_gin_student_column USING GIN(to_tsvector('english', data2)) LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) ;
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_row1 ON test_gin_student_row USING GIN(to_tsvector('english', data1)) LOCAL;
--refer to special partition
CREATE INDEX test_gin_student_index_row2 ON test_gin_student_row USING GIN(to_tsvector('english', data2)) LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) ;
CREATE INDEX test_gin_student_row2_idx ON test_gin_student_row2 USING GIN(info) LOCAL;


--query
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_row WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data2) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_row WHERE to_tsvector('english', data2) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_row2 WHERE info @> '{2}' AND info @> '{200001}' ORDER BY id, info;

--query & check result
SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row2 WHERE info @> '{2}' AND info @> '{200001}' ORDER BY id, info;



--teaeDown drop table
DROP TABLE test_gin_student_row;
DROP TABLE test_gin_student_column;
DROP TABLE test_gin_student_row2;


