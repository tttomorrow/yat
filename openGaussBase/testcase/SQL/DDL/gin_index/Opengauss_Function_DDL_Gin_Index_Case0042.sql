-- @testpoint: create gin index: 多字段索引(4)

SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;

-- column table
DROP TABLE IF EXISTS test_gin_2;
CREATE TABLE test_gin_2 (id INT, first_name text, last_name text, test1 text, test2 text) WITH (ORIENTATION = COLUMN);

--row table
DROP TABLE IF EXISTS test_gin_row1;DROP TABLE IF EXISTS test_gin_row2;
CREATE TABLE test_gin_row2 (id INT, first_name text, last_name text, test1 text, test2 text);

--create gin index
--successfully (COLUMN)
CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector('english', first_name),to_tsvector('english', last_name),to_tsvector('english', test1)) ;
--successfully(row)
CREATE INDEX  test_gin_row2_first_name_idx  ON test_gin_row2 USING GIN(to_tsvector('english', first_name),to_tsvector('english', last_name),to_tsvector('english', test1)) with (FASTUPDATE=off,GIN_PENDING_LIST_LIMIT=64);

--insert data
INSERT INTO test_gin_2 SELECT id, md5(random()::text), md5(random()::text) , md5(random()::text) , md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS id) AS x;
INSERT INTO test_gin_row2 SELECT id, md5(random()::text), md5(random()::text), md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS id) AS x;
INSERT INTO test_gin_2 VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(6, 'Japan is an island country in East Asia.', 'Japan','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France');
INSERT INTO test_gin_2 VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(14, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicox','China', 'China, officially the People');
INSERT INTO test_gin_2 VALUES(15, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicos','China', 'China, officially the People');

INSERT INTO test_gin_row2 VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(6, 'Japan is an island country in East Asia.', 'Japan','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France');
INSERT INTO test_gin_row2 VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(14, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicox','China', 'China, officially the People');
INSERT INTO test_gin_row2 VALUES(15, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexicos','China', 'China, officially the People');


--query
explain SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') and to_tsvector('english', test1) @@ to_tsquery('english', 'China');
SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') and to_tsvector('english', test1) @@ to_tsquery('english', 'China');
explain SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') and to_tsvector('english', test2) @@ to_tsquery('english', 'China');
SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') and to_tsvector('english', test2) @@ to_tsquery('english', 'China');
explain SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') and to_tsvector('english', test2) @@ to_tsquery('english', 'Mexico');
SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') and to_tsvector('english', test2) @@ to_tsquery('english', 'Mexico');

explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') ORDER BY id, first_name, last_name;
SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico') and  to_tsvector('english', last_name) @@ to_tsquery('english', 'Mexico') ORDER BY id, first_name, last_name;
--drop index
drop index test_gin_2_first_name_idx;
drop index test_gin_row2_first_name_idx;

--teaeDown drop table
DROP TABLE IF EXISTS test_gin_2;
DROP TABLE IF EXISTS test_gin_row2;
