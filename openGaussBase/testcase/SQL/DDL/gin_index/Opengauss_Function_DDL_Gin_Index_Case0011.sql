--  @testpoint: create gin index:FASTUPDATE=off,GIN_PENDING_LIST_LIMIT
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

--insert data

INSERT INTO test_gin_student_column SELECT num, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;
INSERT INTO test_gin_student_row SELECT num, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;

--create gin index
--fail
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_column1 ON test_gin_student_column USING GIN(to_tsvector('english', data1)) LOCAL with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=63);
--refer to special partition
CREATE INDEX test_gin_student_index_column2 ON test_gin_student_column USING GIN(to_tsvector('english', data2))  LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=63);
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_row1 ON test_gin_student_row USING GIN(to_tsvector('english', data1)) LOCAL with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=63);
--refer to special partition
CREATE INDEX test_gin_student_index_row2 ON test_gin_student_row USING GIN(to_tsvector('english', data2)) LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=63);

--successfully
CREATE INDEX test_gin_student_index_column1 ON test_gin_student_column USING GIN(to_tsvector('english', data1)) LOCAL with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=1025);
--refer to special partition
CREATE INDEX test_gin_student_index_column2 ON test_gin_student_column USING GIN(to_tsvector('english', data2))  LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=1025);
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_row1 ON test_gin_student_row USING GIN(to_tsvector('english', data1)) LOCAL with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=1025);
--refer to special partition
CREATE INDEX test_gin_student_index_row2 ON test_gin_student_row USING GIN(to_tsvector('english', data2)) LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=1025);
--query
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_row WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data2) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
explain SELECT * FROM test_gin_student_row WHERE to_tsvector('english', data2) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;


--query & check result
SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'test') ORDER BY num, data1, data2;

--tearDown drop table
DROP TABLE test_gin_student_row;
DROP TABLE test_gin_student_column;