--  @testpoint: create gin index:创建gin索引后数据插，数据类型为tevevtor以及数组

-- column table
DROP TABLE IF EXISTS test_gin_2;
CREATE TABLE test_gin_2 (id INT, first_name text, last_name text) WITH (ORIENTATION = COLUMN);

--row table
DROP TABLE IF EXISTS test_gin_row1;
DROP TABLE IF EXISTS test_gin_row2;
CREATE TABLE test_gin_row1 (id INT, info INT[]);
CREATE TABLE test_gin_row2 (id INT, first_name text, last_name text);

--create gin index
--fail(COLUMN)
CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector('english', first_name)) LOCAL;
--successfully(COLUMN)
CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector('english', first_name));
--fail(row)
CREATE INDEX  test_gin_row1_idx ON test_gin_row1 USING GIN(info) LOCAL;
--successfully(row)
CREATE INDEX  test_gin_row1_idx ON test_gin_row1 USING GIN(info);
--successfully(row)
CREATE INDEX  test_gin_row2_first_name_idx  ON test_gin_row2 USING GIN(to_tsvector('english', first_name));


--insert data
INSERT INTO test_gin_2 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS id) AS x;

INSERT INTO test_gin_row1 SELECT g, ARRAY[1, g % 5, g] FROM generate_series(1, 200000) g;
INSERT INTO test_gin_row2 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,200000) AS id) AS x;

--query
explain SELECT * FROM test_gin_2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'test') ORDER BY id, first_name, last_name;
explain SELECT * FROM test_gin_row1 WHERE info @> '{2}' AND info @> '{22}' ORDER BY id, info;
explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'test') ORDER BY id, first_name, last_name;


--teaeDown drop table
DROP TABLE IF EXISTS test_gin_2;
DROP TABLE IF EXISTS test_gin_row1;
DROP TABLE IF EXISTS test_gin_row2;
