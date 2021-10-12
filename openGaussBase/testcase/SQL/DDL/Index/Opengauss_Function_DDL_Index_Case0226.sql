--  @testpoint:事务外使用concurrently删除索引

SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;

-- create table
DROP TABLE IF EXISTS ddl_index_case0226;
CREATE TABLE ddl_index_case0226(id INT, first_name text, last_name text);

--insert data
INSERT INTO ddl_index_case0226 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,2000000) AS id) AS x;
update ddl_index_case0226 set first_name='+dw', last_name='dw_rt' where id = 698;

--create  unique btree index
create UNIQUE index CONCURRENTLY ddl_index_case0226_idx on ddl_index_case0226 USING btree(id);

--drop index concurrently success
drop index concurrently ddl_index_case0226_idx;

--create  unique btree index
create UNIQUE index  ddl_index_case0226_idx on ddl_index_case0226 USING btree(id);

--drop index concurrently success
drop index concurrently ddl_index_case0226_idx;

--explain
explain select * from ddl_index_case0226 where id=698;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0226;

