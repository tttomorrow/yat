-- @testpoint: 查询某一列的注释
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int);
COMMENT ON COLUMN table_test001.c IS 'Primary key of customer demographics table.';
select col_description(oid, 1) from pg_class where relname = 'table_test001';
DROP table IF EXISTS table_test001;
DROP table IF EXISTS table_test002;
create table table_test002(c int,d int);
COMMENT ON COLUMN table_test002.d IS 'this is a comment.';
select col_description(oid, 2) from pg_class where relname = 'table_test002';
DROP table IF EXISTS table_test002;