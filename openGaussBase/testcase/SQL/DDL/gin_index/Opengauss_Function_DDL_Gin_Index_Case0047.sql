--  @testpoint: alter gin index: 表上索引UNUSABLE 索引分区上
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
    data2 text,
    test1 text,
    test2 text
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
    data2 text,
    test1 text,
    test2 text
)
PARTITION BY RANGE(num)
(
    PARTITION num1 VALUES LESS THAN(10000),
    PARTITION num2 VALUES LESS THAN(20000),
    PARTITION num3 VALUES LESS THAN(300000)
);

--create gin index
--refer to special partition
CREATE INDEX test_gin_student_index_column1 ON test_gin_student_column USING GIN(to_tsvector('english', data1),to_tsvector('english', data2),to_tsvector('english', test1),to_tsvector('english', test2)) LOCAL ;
--refer to special partition
CREATE INDEX test_gin_student_index_column2 ON test_gin_student_column USING GIN(to_tsvector('english', data1),to_tsvector('english', data2),to_tsvector('english', test1),to_tsvector('english', test2))  LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) ;
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_row1 ON test_gin_student_row USING GIN(to_tsvector('english', data1),to_tsvector('english', data2),to_tsvector('english', test1),to_tsvector('english', test2)) LOCAL ;
--refer to special partition
CREATE INDEX test_gin_student_index_row2 ON test_gin_student_row USING GIN(to_tsvector('english', data1),to_tsvector('english', data2),to_tsvector('english', test1),to_tsvector('english', test2)) LOCAL
(
    PARTITION data2_index_1 ,
    PARTITION data2_index_2 ,
    PARTITION data2_index_3
) ;

--insert data
INSERT INTO test_gin_student_column SELECT num, md5(random()::text), md5(random()::text) , md5(random()::text) , md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;
INSERT INTO test_gin_student_column VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(6, 'Japan is an island country in East Asia.', 'Japan','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France');
INSERT INTO test_gin_student_column VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(14, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicox','China', 'China, officially the People');
INSERT INTO test_gin_student_column VALUES(20001, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicos','China', 'China, officially the People');

INSERT INTO test_gin_student_row SELECT num, md5(random()::text), md5(random()::text) , md5(random()::text) , md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;
INSERT INTO test_gin_student_row VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(6, 'Japan is an island country in East Asia.', 'Japan','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France');
INSERT INTO test_gin_student_row VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(14, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicox','China', 'China, officially the People');
INSERT INTO test_gin_student_row VALUES(20001, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicos','China', 'China, officially the People');
--alter index UNUSABLE
--fail
alter index test_gin_student_index_column1 UNUSABLE;


--query
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') and to_tsvector('english', test1) @@ to_tsquery('english', 'China');
SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') and to_tsvector('english', test1) @@ to_tsquery('english', 'China');
--successfully
alter index test_gin_student_index_row2 MODIFY PARTITION data2_index_1 UNUSABLE;

--query
--index unable
explain SELECT * FROM test_gin_student_row partition(num1) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row partition(num1) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;
--use index
explain SELECT * FROM test_gin_student_row partition(num2) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row partition(num2) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;
--successfully
alter index test_gin_student_index_row1 UNUSABLE;
--query
explain SELECT * FROM test_gin_student_row partition(num2) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row partition(num2) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;

--successfully
alter index test_gin_student_index_row2 UNUSABLE;
--query
explain SELECT * FROM test_gin_student_row partition(num2) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;
SELECT * FROM test_gin_student_row partition(num2) WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Brazil') and  to_tsvector('english', data2) @@ to_tsquery('english', 'Brazil') ORDER BY num, data1, data2;


--tearDown drop table
DROP TABLE test_gin_student_row;
DROP TABLE test_gin_student_column;