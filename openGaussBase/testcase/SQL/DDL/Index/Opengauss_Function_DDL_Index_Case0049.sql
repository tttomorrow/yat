--  @testpoint: 唯一索引：行存表gin索引不支持：普通表：合理报错
--建表
DROP TABLE if EXISTS test_index_table_049 CASCADE;
create table test_index_table_049(id int, body text, title text, last_mod_date date) with (ORIENTATION = column);
--插入数据
INSERT INTO test_index_table_049 VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China', '2010-1-1');

DROP INDEX IF EXISTS index_049;
CREATE unique INDEX index_049 ON test_index_table_049 USING gin(to_tsvector('english', body));
--清理数据
DROP TABLE if EXISTS test_index_table_049 CASCADE;