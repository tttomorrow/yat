-- @testpoint: create gin index: FASTUPDATE=on,GIN_PENDING_LIST_LIMIT合理报错

SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;

-- column table
DROP TABLE IF EXISTS test_gin_2;
CREATE TABLE test_gin_2 (id INT, first_name text, last_name text) WITH (ORIENTATION = COLUMN);

--row table
DROP TABLE IF EXISTS test_gin_row1;
DROP TABLE IF EXISTS test_gin_row2;
CREATE TABLE test_gin_row1 (id INT, info INT[]);
CREATE TABLE test_gin_row2 (id INT, first_name text, last_name text);


--insert data
INSERT INTO test_gin_2 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,2000000) AS id) AS x;

INSERT INTO test_gin_row1 SELECT g, ARRAY[1, g % 5, g] FROM generate_series(1, 200000) g;
INSERT INTO test_gin_row2 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS id) AS x;

--create gin index
--fail(COLUMN)
CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector('english', first_name)) with (FASTUPDATE=on,GIN_PENDING_LIST_LIMIT=63);
--fail (row)
CREATE INDEX  test_gin_row1_idx ON test_gin_row1 USING GIN(info) with (FASTUPDATE=on, GIN_PENDING_LIST_LIMIT=63);
--fail(row)
CREATE INDEX  test_gin_row2_first_name_idx  ON test_gin_row2 USING GIN(to_tsvector('english', first_name)) with (FASTUPDATE=on,GIN_PENDING_LIST_LIMIT=63);
--fail(COLUMN)
--fail (row)
--fail(row)
--successfully (COLUMN)
CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector('english', first_name)) with (FASTUPDATE=on,GIN_PENDING_LIST_LIMIT=64);
--successfully (row)
CREATE INDEX  test_gin_row1_idx ON test_gin_row1 USING GIN(info) with (FASTUPDATE=on, GIN_PENDING_LIST_LIMIT=64);
--successfully(row)
CREATE INDEX  test_gin_row2_first_name_idx  ON test_gin_row2 USING GIN(to_tsvector('english', first_name)) with (FASTUPDATE=on,GIN_PENDING_LIST_LIMIT=64);
--query
explain SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'test') ORDER BY id, first_name, last_name;
explain SELECT * FROM test_gin_row1 WHERE info @> '{2}' AND info @> '{22}' ORDER BY id, info;
explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'test') ORDER BY id, first_name, last_name;
--drop index
drop index test_gin_2_first_name_idx;
drop index test_gin_row1_idx;
drop index test_gin_row2_first_name_idx;

--successfully (COLUMN)
CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector('english', first_name)) with (FASTUPDATE=on,GIN_PENDING_LIST_LIMIT=1025);
--successfully (row)
CREATE INDEX  test_gin_row1_idx ON test_gin_row1 USING GIN(info) with (FASTUPDATE=on, GIN_PENDING_LIST_LIMIT=1025);
--successfully(row)
CREATE INDEX  test_gin_row2_first_name_idx  ON test_gin_row2 USING GIN(to_tsvector('english', first_name)) with (FASTUPDATE=on,GIN_PENDING_LIST_LIMIT=1025);
--insert data
INSERT INTO test_gin_2 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200) AS id) AS x;

INSERT INTO test_gin_row1 SELECT g, ARRAY[1, g % 5, g] FROM generate_series(1, 200) g;
INSERT INTO test_gin_row2 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200) AS id) AS x;

--query
explain SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'test') ORDER BY id, first_name, last_name;
explain SELECT * FROM test_gin_row1 WHERE info @> '{2}' AND info @> '{22}' ORDER BY id, info;
explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'test') ORDER BY id, first_name, last_name;

--teaeDown drop table
DROP TABLE IF EXISTS test_gin_2;
DROP TABLE IF EXISTS test_gin_row1;
DROP TABLE IF EXISTS test_gin_row2;
