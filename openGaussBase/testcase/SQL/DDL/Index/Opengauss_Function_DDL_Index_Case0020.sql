-- @testpoint:  USING method：行存表gin索引20：success
--建表
DROP TABLE if EXISTS test_index_table_020 CASCADE;

CREATE TABLE test_index_table_020 (id int, body text, title text, last_mod_date date);

INSERT INTO test_index_table_020 VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(6, 'Japan is an island country in East Asia.', 'Japan', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.', 'Germany', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada', '2010-1-1');
INSERT INTO test_index_table_020 VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico', '2010-1-1');


SELECT id, body, title FROM test_index_table_020 WHERE to_tsvector('english', body) @@ to_tsquery('english', 'america');
--查看参数，设置索引
--GUC参数default_text_search_config指定了默认的文本搜索配置
SHOW default_text_search_config;
drop index if exists gin_index_01;
CREATE INDEX gin_index_01 ON test_index_table_020 USING gin(to_tsvector('english', body));

explain SELECT id, body, title FROM test_index_table_020 WHERE to_tsvector('english', body) @@ to_tsquery('english', 'america');
select relname from pg_class where relname='gin_index_01';

drop index if exists gin_index_01;
DROP TABLE if EXISTS test_index_table_020 CASCADE;