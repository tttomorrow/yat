-- @testpoint: drop index concurrently 不支持事务内 合理报错

-- create table
DROP TABLE IF EXISTS ddl_index_case0228;
CREATE TABLE ddl_index_case0228(id INT, first_name text, last_name text);

--create  index
create  index CONCURRENTLY ddl_index_case0228_idx on ddl_index_case0228 USING btree(id);

-- start transaction
START TRANSACTION;
--drop index concurrently success
drop index concurrently ddl_index_case0228_idx;
-- end transaction
end;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0228;