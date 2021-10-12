--  @testpoint: column_name：列存分区表常用数据类型1列：successs
DROP TABLE if EXISTS test_index_table_061_01 CASCADE;
DROP TABLE if EXISTS test_index_table_061_02 CASCADE;
DROP TABLE if EXISTS test_index_table_061_03 CASCADE;
DROP TABLE if EXISTS test_index_table_061_04 CASCADE;
DROP TABLE if EXISTS test_index_table_061_05 CASCADE;
DROP TABLE if EXISTS test_index_table_061_06 CASCADE;
DROP TABLE if EXISTS test_index_table_061_07 CASCADE;
DROP TABLE if EXISTS test_index_table_061_08 CASCADE;
DROP TABLE if EXISTS test_index_table_061_09 CASCADE;
DROP TABLE if EXISTS test_index_table_061_10 CASCADE;

create table test_index_table_061_01(c_int INTEGER) WITH (ORIENTATION = column) PARTITION BY RANGE(c_int)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_061_02(c_numeric NUMERIC) WITH (ORIENTATION = column) PARTITION BY RANGE(c_numeric)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_061_03(c_float FLOAT) WITH (ORIENTATION = column) PARTITION BY RANGE(c_float)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_061_06(c_char CHAR) WITH (ORIENTATION = column) PARTITION BY RANGE(c_char)(PARTITION P1 VALUES LESS THAN(1));
create table test_index_table_061_07(c_varchar VARCHAR) WITH (ORIENTATION = column) PARTITION BY RANGE(c_varchar)(PARTITION P1 VALUES LESS THAN(100));
create table test_index_table_061_08(c_clob CLOB) WITH (ORIENTATION = column) PARTITION BY RANGE(c_clob)(
PARTITION P1 VALUES LESS THAN('g'),
PARTITION P2 VALUES LESS THAN('z')
);
create table test_index_table_061_09(c_text TEXT) WITH (ORIENTATION = column) PARTITION BY RANGE(c_text)(
PARTITION P1 VALUES LESS THAN('g'),
PARTITION P2 VALUES LESS THAN('z')
);
create table test_index_table_061_10(c_date DATE) WITH (ORIENTATION = column) PARTITION BY RANGE(c_date)(PARTITION P1 VALUES LESS THAN('1900-01-01 00:00:00'));


--建psort索引
drop index if exists index_061_01;
drop index if exists index_061_02;
drop index if exists index_061_03;
drop index if exists index_061_04;
drop index if exists index_061_05;
drop index if exists index_061_06;
drop index if exists index_061_07;
drop index if exists index_061_08;
drop index if exists index_061_09;
drop index if exists index_061_10;

create index index_061_01 on test_index_table_061_01(c_int) local;
create index index_061_02 on test_index_table_061_02(c_numeric) local;
create index index_061_03 on test_index_table_061_03(c_float) local;
create index index_061_06 on test_index_table_061_06(c_char) local;
create index index_061_07 on test_index_table_061_07(c_varchar) local;
create index index_061_08 on test_index_table_061_08(c_clob) local;
create index index_061_09 on test_index_table_061_09(c_text) local;
create index index_061_10 on test_index_table_061_10(c_date) local;

select relname from pg_class where relname like 'index_061_%' order by relname;

--btree
drop index if exists index_061_01;
drop index if exists index_061_02;
drop index if exists index_061_03;
drop index if exists index_061_04;
drop index if exists index_061_05;
drop index if exists index_061_06;
drop index if exists index_061_07;
drop index if exists index_061_08;
drop index if exists index_061_09;
drop index if exists index_061_10;

create index index_061_01 on test_index_table_061_01 using btree(c_int) local;
create index index_061_02 on test_index_table_061_02 using btree(c_numeric) local;
create index index_061_03 on test_index_table_061_03 using btree(c_float) local;
create index index_061_06 on test_index_table_061_06 using btree(c_char) local;
create index index_061_07 on test_index_table_061_07 using btree(c_varchar) local;
create index index_061_08 on test_index_table_061_08 using btree(c_clob) local;
create index index_061_09 on test_index_table_061_09 using btree(c_text) local;
create index index_061_10 on test_index_table_061_10 using btree(c_date) local;

select relname from pg_class where relname like 'index_061_%' order by relname;

--gin
drop index if exists index_061_01;
drop index if exists index_061_02;
drop index if exists index_061_03;
drop index if exists index_061_04;
drop index if exists index_061_05;
drop index if exists index_061_06;
drop index if exists index_061_07;
drop index if exists index_061_08;
drop index if exists index_061_09;
drop index if exists index_061_10;

create index index_061_01 on test_index_table_061_01 using gin(to_tsvector('english', c_int)) local;
create index index_061_02 on test_index_table_061_02 using gin(to_tsvector('english', c_numeric)) local;
create index index_061_03 on test_index_table_061_03 using gin(to_tsvector('english', c_float)) local;
create index index_061_06 on test_index_table_061_06 using gin(to_tsvector('english', c_char)) local;
create index index_061_07 on test_index_table_061_07 using gin(to_tsvector('english', c_varchar)) local;
create index index_061_08 on test_index_table_061_08 using gin(to_tsvector('english', c_clob)) local;
create index index_061_09 on test_index_table_061_09 using gin(to_tsvector('english', c_text)) local;
create index index_061_10 on test_index_table_061_10 using gin(to_tsvector('english', c_date)) local;
select relname from pg_class where relname like 'index_061_%' order by relname;
--清理环境
drop index if exists index_061_01;
drop index if exists index_061_02;
drop index if exists index_061_03;
drop index if exists index_061_04;
drop index if exists index_061_05;
drop index if exists index_061_06;
drop index if exists index_061_07;
drop index if exists index_061_08;
drop index if exists index_061_09;
drop index if exists index_061_10;
DROP TABLE if EXISTS test_index_table_061_01 CASCADE;
DROP TABLE if EXISTS test_index_table_061_02 CASCADE;
DROP TABLE if EXISTS test_index_table_061_03 CASCADE;
DROP TABLE if EXISTS test_index_table_061_04 CASCADE;
DROP TABLE if EXISTS test_index_table_061_05 CASCADE;
DROP TABLE if EXISTS test_index_table_061_06 CASCADE;
DROP TABLE if EXISTS test_index_table_061_07 CASCADE;
DROP TABLE if EXISTS test_index_table_061_08 CASCADE;
DROP TABLE if EXISTS test_index_table_061_09 CASCADE;
DROP TABLE if EXISTS test_index_table_061_10 CASCADE;
