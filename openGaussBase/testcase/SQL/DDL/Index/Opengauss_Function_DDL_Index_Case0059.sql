--  @testpoint:--column_name：列存普通表常用数据类型1列：successs
DROP TABLE if EXISTS test_index_table_059 CASCADE;
create table test_index_table_059(
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
) WITH (ORIENTATION = column);

--建psort索引
drop index if exists index_059_01;
drop index if exists index_059_02;
drop index if exists index_059_03;
drop index if exists index_059_04;
drop index if exists index_059_05;
drop index if exists index_059_06;
drop index if exists index_059_07;
drop index if exists index_059_08;
drop index if exists index_059_09;
drop index if exists index_059_10;

create index index_059_01 on test_index_table_059(c_int);
create index index_059_02 on test_index_table_059(c_numeric);
create index index_059_03 on test_index_table_059(c_float);
create index index_059_04 on test_index_table_059(c_money);
create index index_059_05 on test_index_table_059(c_boolean);
create index index_059_06 on test_index_table_059(c_char);
create index index_059_07 on test_index_table_059(c_varchar);
create index index_059_08 on test_index_table_059(c_clob);
create index index_059_09 on test_index_table_059(c_text);
create index index_059_10 on test_index_table_059(c_date);

select relname from pg_class where relname like 'index_059_%' order by relname;

--btree
drop index if exists index_059_01;
drop index if exists index_059_02;
drop index if exists index_059_03;
drop index if exists index_059_04;
drop index if exists index_059_05;
drop index if exists index_059_06;
drop index if exists index_059_07;
drop index if exists index_059_08;
drop index if exists index_059_09;
drop index if exists index_059_10;

create index index_059_01 on test_index_table_059 using btree(c_int);
create index index_059_02 on test_index_table_059 using btree(c_numeric);
create index index_059_03 on test_index_table_059 using btree(c_float);
create index index_059_04 on test_index_table_059 using btree(c_money);
create index index_059_05 on test_index_table_059 using btree(c_boolean);
create index index_059_06 on test_index_table_059 using btree(c_char);
create index index_059_07 on test_index_table_059 using btree(c_varchar);
create index index_059_08 on test_index_table_059 using btree(c_clob);
create index index_059_09 on test_index_table_059 using btree(c_text);
create index index_059_10 on test_index_table_059 using btree(c_date);

select relname from pg_class where relname like 'index_059_%' order by relname;

--gin
drop index if exists index_059_01;
drop index if exists index_059_02;
drop index if exists index_059_03;
drop index if exists index_059_04;
drop index if exists index_059_05;
drop index if exists index_059_06;
drop index if exists index_059_07;
drop index if exists index_059_08;
drop index if exists index_059_09;
drop index if exists index_059_10;

create index index_059_01 on test_index_table_059 using gin(to_tsvector('english', c_int));
create index index_059_02 on test_index_table_059 using gin(to_tsvector('english', c_numeric));
create index index_059_03 on test_index_table_059 using gin(to_tsvector('english', c_float));
create index index_059_06 on test_index_table_059 using gin(to_tsvector('english', c_char));
create index index_059_07 on test_index_table_059 using gin(to_tsvector('english', c_varchar));
create index index_059_08 on test_index_table_059 using gin(to_tsvector('english', c_clob));
create index index_059_09 on test_index_table_059 using gin(to_tsvector('english', c_text));
create index index_059_10 on test_index_table_059 using gin(to_tsvector('english', c_date));
select relname from pg_class where relname like 'index_059_%' order by relname;
--清理环境
drop index if exists index_059_01;
drop index if exists index_059_02;
drop index if exists index_059_03;
drop index if exists index_059_04;
drop index if exists index_059_05;
drop index if exists index_059_06;
drop index if exists index_059_07;
drop index if exists index_059_08;
drop index if exists index_059_09;
drop index if exists index_059_10;
DROP TABLE if EXISTS test_index_table_059 CASCADE;
