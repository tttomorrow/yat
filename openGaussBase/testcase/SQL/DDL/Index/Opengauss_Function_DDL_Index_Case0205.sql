--  @testpoint: 创建临时表使用concurrently创建索引


SET ENABLE_SEQSCAN=off;
RESET ENABLE_INDEXSCAN;
RESET ENABLE_BITMAPSCAN;

show ENABLE_SEQSCAN;
show ENABLE_INDEXSCAN;
show ENABLE_BITMAPSCAN;

-- create global tmp table
DROP TABLE IF EXISTS ddl_index_case0205;
CREATE  GLOBAL TEMPORARY TABLE ddl_index_case0205(id INT, first_name text, last_name text);

--insert data
INSERT INTO ddl_index_case0205 SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,2000000) AS id) AS x;
update ddl_index_case0205 set first_name='+dw', last_name='dw_rt' where id = 698;

--create  index
create  index CONCURRENTLY ddl_index_case0205_idx on ddl_index_case0205 USING btree(id);

--explain
explain select * from ddl_index_case0205 where id=698;

--select
select * from ddl_index_case0205 where id=698;
select pg_sleep(3);
-- create local tmp table
DROP TABLE IF EXISTS ddl_index_case0205_local;
CREATE  TEMPORARY TABLE ddl_index_case0205_local(id INT, first_name text, last_name text);

--insert data
INSERT INTO ddl_index_case0205_local SELECT id, md5(random()::text), md5(random()::text) FROM (SELECT * FROM generate_series(1,2000000) AS id) AS x;
update ddl_index_case0205_local set first_name='+dw', last_name='dw_rt' where id = 698;
select pg_sleep(3);
--create  index
create  index CONCURRENTLY ddl_index_case0205_local_idx on ddl_index_case0205_local USING btree(id);
select pg_sleep(3);
--explain
explain select * from ddl_index_case0205_local where id=698;

--select
select * from ddl_index_case0205_local where id=698;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0205;
DROP TABLE IF EXISTS ddl_index_case0205_local;
