--  @testpoint: column_name：行存分区表各数据类型1列：successs
--建表

DROP TABLE if EXISTS test_index_table_058_02 CASCADE;
DROP TABLE if EXISTS test_index_table_058_03 CASCADE;
DROP TABLE if EXISTS test_index_table_058_04 CASCADE;
DROP TABLE if EXISTS test_index_table_058_05 CASCADE;
DROP TABLE if EXISTS test_index_table_058_06 CASCADE;
DROP TABLE if EXISTS test_index_table_058_07 CASCADE;
DROP TABLE if EXISTS test_index_table_058_08 CASCADE;
DROP TABLE if EXISTS test_index_table_058_09 CASCADE;
DROP TABLE if EXISTS test_index_table_058_10 CASCADE;
DROP TABLE if EXISTS test_index_table_058_11 CASCADE;
DROP TABLE if EXISTS test_index_table_058_13 CASCADE;

create table test_index_table_058_02(name BIGINT) WITH (ORIENTATION = row) PARTITION BY RANGE(name)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_03(name NUMERIC) WITH (ORIENTATION = row) PARTITION BY RANGE(name)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_04(name NUMBER) WITH (ORIENTATION = row) PARTITION BY RANGE(name)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_05(name SMALLSERIAL) WITH (ORIENTATION = row) PARTITION BY RANGE(name)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_06(name SERIAL) WITH (ORIENTATION = row) PARTITION BY RANGE(name)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_07(name BIGSERIAL) WITH (ORIENTATION = row) PARTITION BY RANGE(name) (PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_08(name BINARY_DOUBLE) WITH (ORIENTATION = row) PARTITION BY RANGE(name)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_09(name DEC) WITH (ORIENTATION = row) PARTITION BY RANGE(name) (PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_10(name CHAR) WITH (ORIENTATION = row) PARTITION BY RANGE(name) (PARTITION P1 VALUES LESS THAN(1));
create table test_index_table_058_11(name VARCHAR) WITH (ORIENTATION = row) PARTITION BY RANGE(name) (PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_058_13(name TEXT) WITH (ORIENTATION = row) PARTITION BY RANGE(name)  (PARTITION P1 VALUES LESS THAN(100));



--建索引
drop INDEX if exists index_058_02,index_058_03,index_058_04,index_058_05;
drop INDEX if exists index_058_06,index_058_07,index_058_08,index_058_09;
drop INDEX if exists index_058_10,index_058_11,index_058_13;

create index index_058_02 on test_index_table_058_02(name);
create index index_058_03 on test_index_table_058_03(name);
create index index_058_04 on test_index_table_058_04(name);
create index index_058_05 on test_index_table_058_05(name);
create index index_058_06 on test_index_table_058_06(name);
create index index_058_07 on test_index_table_058_07(name);
create index index_058_08 on test_index_table_058_08(name);
create index index_058_09 on test_index_table_058_09(name);
create index index_058_10 on test_index_table_058_10(name);
create index index_058_11 on test_index_table_058_11(name);
create index index_058_13 on test_index_table_058_13(name);

--查索引
select relname from pg_class where relname like 'index_058_%';


--gin索引
drop INDEX if exists index_058_02,index_058_03,index_058_04,index_058_05;
drop INDEX if exists index_058_06,index_058_07,index_058_08,index_058_09;
drop INDEX if exists index_058_10,index_058_11,index_058_13;

create index index_058_02 on test_index_table_058_02 using gin(to_tsvector('english', name)) local;
create index index_058_03 on test_index_table_058_03 using gin(to_tsvector('english', name)) local;
create index index_058_04 on test_index_table_058_04 using gin(to_tsvector('english', name)) local;
create index index_058_05 on test_index_table_058_05 using gin(to_tsvector('english', name)) local;
create index index_058_06 on test_index_table_058_06 using gin(to_tsvector('english', name)) local;
create index index_058_07 on test_index_table_058_07 using gin(to_tsvector('english', name)) local;
create index index_058_08 on test_index_table_058_08 using gin(to_tsvector('english', name)) local;
create index index_058_09 on test_index_table_058_09 using gin(to_tsvector('english', name)) local;
create index index_058_10 on test_index_table_058_10 using gin(to_tsvector('english', name)) local;
create index index_058_11 on test_index_table_058_11 using gin(to_tsvector('english', name)) local;
create index index_058_13 on test_index_table_058_13 using gin(to_tsvector('english', name)) local;

--查索引
select relname from pg_class where relname like 'index_058_%';

--清理数据
DROP TABLE if EXISTS test_index_table_058_02 CASCADE;
DROP TABLE if EXISTS test_index_table_058_03 CASCADE;
DROP TABLE if EXISTS test_index_table_058_04 CASCADE;
DROP TABLE if EXISTS test_index_table_058_05 CASCADE;
DROP TABLE if EXISTS test_index_table_058_06 CASCADE;
DROP TABLE if EXISTS test_index_table_058_07 CASCADE;
DROP TABLE if EXISTS test_index_table_058_08 CASCADE;
DROP TABLE if EXISTS test_index_table_058_09 CASCADE;
DROP TABLE if EXISTS test_index_table_058_10 CASCADE;
DROP TABLE if EXISTS test_index_table_058_11 CASCADE;
DROP TABLE if EXISTS test_index_table_058_13 CASCADE;
