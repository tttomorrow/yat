--  @testpoint:使用concurrently删除gin gist索引

-- create table
DROP TABLE IF EXISTS ddl_index_case0230;
CREATE TABLE ddl_index_case0230(id INT, first_name text, last_name text);

--create  gin index
create  index CONCURRENTLY ddl_index_case0230_idx on ddl_index_case0230 USING gin(to_tsvector('english', first_name));

--drop index
drop index concurrently ddl_index_case0230_idx;

-- create table
DROP TABLE IF EXISTS ddl_index_case0230_gist;
CREATE TABLE ddl_index_case0230_gist(id INT, c_point point);

--create  gist index
create  index CONCURRENTLY ddl_index_case0230_idx_gist on ddl_index_case0230_gist  USING gist(c_point);

--drop index
drop index concurrently ddl_index_case0230_idx_gist;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0230;
DROP TABLE IF EXISTS ddl_index_case0230_gist;