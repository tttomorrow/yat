--  @testpoint:drop concurrently 临时表

-- create global tmp table
DROP TABLE IF EXISTS ddl_index_case0229;
CREATE  GLOBAL TEMPORARY TABLE ddl_index_case0229(id INT, first_name text, last_name text);

--create  index
create  index ddl_index_case0229_idx on ddl_index_case0229 USING btree(id);

--drop index
drop index concurrently ddl_index_case0229_idx;

-- create local tmp table
DROP TABLE IF EXISTS ddl_index_case0229_local;
CREATE  TEMPORARY TABLE ddl_index_case0229_local(id INT, first_name text, last_name text);

--create  index
create  index CONCURRENTLY ddl_index_case0229_local_idx on ddl_index_case0229_local USING btree(id);

--drop index
drop index concurrently ddl_index_case0229_local_idx;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0229;
DROP TABLE IF EXISTS ddl_index_case0229_local;