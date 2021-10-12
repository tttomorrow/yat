--  @testpoint: 事务外使用concurrently创建索引

SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;

-- create table
DROP TABLE IF EXISTS ddl_index_case0204;
CREATE TABLE ddl_index_case0204(id INT, first_name text, last_name text);

--insert data
INSERT INTO ddl_index_case0204 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,2000000) AS id) AS x;
update ddl_index_case0204 set first_name='+dw', last_name='dw_rt' where id = 698;

--create  index
create UNIQUE index CONCURRENTLY ddl_index_case0204_idx on ddl_index_case0204 USING btree(id);

--explain
explain select * from ddl_index_case0204 where id=698;

--select
select * from ddl_index_case0204 where id=698;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0204;