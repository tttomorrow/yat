--  @testpoint: column_name：行存普通表常用数据类型3列：successs
DROP TABLE if EXISTS test_index_table_062 CASCADE;
create table test_index_table_062(
c_int INTEGER,
c_numeric NUMERIC,
c_float FLOAT,
c_money money,
c_boolean BOOLEAN,
c_char CHAR,
c_varchar VARCHAR,
c_clob CLOB,
c_text TEXT,
c_date DATE
) WITH (ORIENTATION = row);

--建psort索引
drop index if exists index_062_01;
drop index if exists index_062_02;
drop index if exists index_062_03;
drop index if exists index_062_04;
drop index if exists index_062_05;
drop index if exists index_062_06;
drop index if exists index_062_07;
drop index if exists index_062_08;
drop index if exists index_062_09;
drop index if exists index_062_10;

create index index_062_01 on test_index_table_062(c_int,c_numeric,c_float);
create index index_062_02 on test_index_table_062(c_numeric,c_float,c_money);
create index index_062_03 on test_index_table_062(c_float,c_money,c_boolean);
create index index_062_04 on test_index_table_062(c_money,c_boolean,c_boolean);
create index index_062_05 on test_index_table_062(c_boolean,c_char,c_varchar);
create index index_062_06 on test_index_table_062(c_char,c_varchar,c_clob);
create index index_062_07 on test_index_table_062(c_varchar,c_clob,c_text);
create index index_062_08 on test_index_table_062(c_clob,c_text,c_date);
create index index_062_09 on test_index_table_062(c_text,c_date,c_numeric);
create index index_062_10 on test_index_table_062(c_date,c_numeric,c_float);

select relname from pg_class where relname like 'index_062_%' order by relname;

--btree
drop index if exists index_062_01;
drop index if exists index_062_02;
drop index if exists index_062_03;
drop index if exists index_062_04;
drop index if exists index_062_05;
drop index if exists index_062_06;
drop index if exists index_062_07;
drop index if exists index_062_08;
drop index if exists index_062_09;
drop index if exists index_062_10;

create index index_062_01 on test_index_table_062 using btree(c_int,c_numeric,c_float);
create index index_062_02 on test_index_table_062 using btree(c_numeric,c_float,c_money);
create index index_062_03 on test_index_table_062 using btree(c_float,c_money,c_boolean);
create index index_062_04 on test_index_table_062 using btree(c_money,c_boolean,c_boolean);
create index index_062_05 on test_index_table_062 using btree(c_boolean,c_char,c_varchar);
create index index_062_06 on test_index_table_062 using btree(c_char,c_varchar,c_clob);
create index index_062_07 on test_index_table_062 using btree(c_varchar,c_clob,c_text);
create index index_062_08 on test_index_table_062 using btree(c_clob,c_text,c_date);
create index index_062_09 on test_index_table_062 using btree(c_text,c_date,c_numeric);
create index index_062_10 on test_index_table_062 using btree(c_date,c_numeric,c_float);

select relname from pg_class where relname like 'index_062_%' order by relname;

--gin
drop index if exists index_062_01;
drop index if exists index_062_02;
drop index if exists index_062_03;
drop index if exists index_062_04;
drop index if exists index_062_05;
drop index if exists index_062_06;
drop index if exists index_062_07;
drop index if exists index_062_08;
drop index if exists index_062_09;
drop index if exists index_062_10;

create index index_062_01 on test_index_table_062 using gin(to_tsvector('english', c_int),to_tsvector('english', c_numeric),to_tsvector('english', c_float));
create index index_062_02 on test_index_table_062 using gin(to_tsvector('english', c_float),to_tsvector('english', c_varchar),to_tsvector('english', c_char));
create index index_062_03 on test_index_table_062 using gin(to_tsvector('english', c_clob),to_tsvector('english', c_numeric),to_tsvector('english', c_date));
create index index_062_04 on test_index_table_062 using gin(to_tsvector('english', c_int),to_tsvector('english', c_clob),to_tsvector('english', c_date));
create index index_062_05 on test_index_table_062 using gin(to_tsvector('english', c_clob),to_tsvector('english', c_numeric),to_tsvector('english', c_date));
create index index_062_06 on test_index_table_062 using gin(to_tsvector('english', c_date),to_tsvector('english', c_numeric),to_tsvector('english', c_float));

select relname from pg_class where relname like 'index_062_%' order by relname;

--清理环境
drop index if exists index_062_01;
drop index if exists index_062_02;
drop index if exists index_062_03;
drop index if exists index_062_04;
drop index if exists index_062_05;
drop index if exists index_062_06;
drop index if exists index_062_07;
drop index if exists index_062_08;
drop index if exists index_062_09;
drop index if exists index_062_10;
DROP TABLE if EXISTS test_index_table_062 CASCADE;