--  @testpoint: create gin index:在同一分区列上多个索引
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

--insert data

INSERT INTO test_gin_student_column SELECT num, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS num) AS x;
INSERT INTO test_gin_student_column VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China');
INSERT INTO test_gin_student_column VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America');
INSERT INTO test_gin_student_column VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England');
INSERT INTO test_gin_student_column VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia');
INSERT INTO test_gin_student_column VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia');
INSERT INTO test_gin_student_column VALUES(6, 'Japan is an island country in East Asia.', 'Japan');
INSERT INTO test_gin_student_column VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.');
INSERT INTO test_gin_student_column VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France');
INSERT INTO test_gin_student_column VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy');
INSERT INTO test_gin_student_column VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India');
INSERT INTO test_gin_student_column VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil');
INSERT INTO test_gin_student_column VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada');
INSERT INTO test_gin_student_column VALUES(5001, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico');

--create gin index
--didn't refer to special partition 
CREATE INDEX test_gin_student_index_column1 ON test_gin_student_column USING GIN(to_tsvector('english', data1)) LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) ;
--refer to special partition
CREATE INDEX test_gin_student_index_column2 ON test_gin_student_column USING GIN(to_tsvector('english', data1)) LOCAL
(
    PARTITION data2_index_1,
    PARTITION data2_index_2,
    PARTITION data2_index_3 
) ;

--query
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Mexico') ORDER BY num, data1, data2;

--reindex
reindex index test_gin_student_index_column2;
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Mexico') ORDER BY num, data1, data2;

--alter index
alter index test_gin_student_index_column2 rename partition data2_index_2 to data2_index_22;
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Mexico') ORDER BY num, data1, data2;

--drop index
drop index test_gin_student_index_column2;
explain SELECT * FROM test_gin_student_column WHERE to_tsvector('english', data1) @@ to_tsquery('english', 'Mexico') ORDER BY num, data1, data2;

--teaeDown drop table
DROP TABLE test_gin_student_column;
