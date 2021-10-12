--  @testpoint: column_name：列存普通表常用数据类型3列：successs
DROP TABLE if EXISTS test_index_table_065 CASCADE;
create table test_index_table_065(
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
drop index if exists index_065_01;
drop index if exists index_065_02;
drop index if exists index_065_03;
drop index if exists index_065_04;
drop index if exists index_065_05;
drop index if exists index_065_06;
drop index if exists index_065_07;
drop index if exists index_065_08;
drop index if exists index_065_09;
drop index if exists index_065_10;

create index index_065_01 on test_index_table_065(c_int,c_numeric,c_float);
create index index_065_02 on test_index_table_065(c_numeric,c_float,c_money);
create index index_065_03 on test_index_table_065(c_float,c_boolean,c_boolean);
create index index_065_04 on test_index_table_065(c_money,c_boolean,c_boolean);
create index index_065_05 on test_index_table_065(c_boolean,c_boolean,c_boolean);
create index index_065_06 on test_index_table_065(c_char,c_boolean,c_boolean);
create index index_065_07 on test_index_table_065(c_varchar,c_boolean,c_char);
create index index_065_08 on test_index_table_065(c_boolean,c_text,c_char);
create index index_065_09 on test_index_table_065(c_text,c_char,c_money);
create index index_065_10 on test_index_table_065(c_date,c_text,c_char);

select relname from pg_class where relname like 'index_065_%' order by relname;

--btree
drop index if exists index_065_01;
drop index if exists index_065_02;
drop index if exists index_065_03;
drop index if exists index_065_04;
drop index if exists index_065_05;
drop index if exists index_065_06;
drop index if exists index_065_07;
drop index if exists index_065_08;
drop index if exists index_065_09;
drop index if exists index_065_10;

create index index_065_01 on test_index_table_065 using btree(c_int,c_numeric,c_float);
create index index_065_02 on test_index_table_065 using btree(c_numeric,c_float,c_money);
create index index_065_03 on test_index_table_065 using btree(c_float,c_boolean,c_boolean);
create index index_065_04 on test_index_table_065 using btree(c_money,c_boolean,c_boolean);
create index index_065_05 on test_index_table_065 using btree(c_boolean,c_boolean,c_boolean);
create index index_065_06 on test_index_table_065 using btree(c_char,c_boolean,c_boolean);
create index index_065_07 on test_index_table_065 using btree(c_varchar,c_boolean,c_char);
create index index_065_08 on test_index_table_065 using btree(c_boolean,c_text,c_char);
create index index_065_09 on test_index_table_065 using btree(c_text,c_char,c_money);
create index index_065_10 on test_index_table_065 using btree(c_date,c_text,c_char);


select relname from pg_class where relname like 'index_065_%' order by relname;

--gin
drop index if exists index_065_01;
drop index if exists index_065_02;
drop index if exists index_065_03;
drop index if exists index_065_04;
drop index if exists index_065_05;
drop index if exists index_065_06;
drop index if exists index_065_07;
drop index if exists index_065_08;
drop index if exists index_065_09;
drop index if exists index_065_10;

create index index_065_01 on test_index_table_065 using gin(to_tsvector('english', c_int),to_tsvector('english', c_numeric),to_tsvector('english', c_float));
create index index_065_02 on test_index_table_065 using gin(to_tsvector('english', c_float),to_tsvector('english', c_varchar),to_tsvector('english', c_char));
create index index_065_03 on test_index_table_065 using gin(to_tsvector('english', c_clob),to_tsvector('english', c_numeric),to_tsvector('english', c_date));
create index index_065_06 on test_index_table_065 using gin(to_tsvector('english', c_int),to_tsvector('english', c_clob),to_tsvector('english', c_date));
create index index_065_07 on test_index_table_065 using gin(to_tsvector('english', c_clob),to_tsvector('english', c_numeric),to_tsvector('english', c_date));
create index index_065_08 on test_index_table_065 using gin(to_tsvector('english', c_date),to_tsvector('english', c_numeric),to_tsvector('english', c_float));

select relname from pg_class where relname like 'index_065_%' order by relname;
--清理环境
drop index if exists index_065_01;
drop index if exists index_065_02;
drop index if exists index_065_03;
drop index if exists index_065_04;
drop index if exists index_065_05;
drop index if exists index_065_06;
drop index if exists index_065_07;
drop index if exists index_065_08;
drop index if exists index_065_09;
drop index if exists index_065_10;
DROP TABLE if EXISTS test_index_table_065 CASCADE;