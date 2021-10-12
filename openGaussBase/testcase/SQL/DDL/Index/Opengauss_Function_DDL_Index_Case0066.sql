--  @testpoint: column_name：列存临时表常用数据类型3列：successs
DROP TABLE if EXISTS test_index_table_066 CASCADE;
create TEMPORARY table test_index_table_066(
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
drop index if exists index_066_01;
drop index if exists index_066_02;
drop index if exists index_066_03;
drop index if exists index_066_04;
drop index if exists index_066_05;
drop index if exists index_066_06;
drop index if exists index_066_07;
drop index if exists index_066_08;
drop index if exists index_066_09;
drop index if exists index_066_10;

create index index_066_01 on test_index_table_066(c_int,c_numeric,c_float);
create index index_066_02 on test_index_table_066(c_numeric,c_float,c_money);
create index index_066_03 on test_index_table_066(c_float,c_boolean,c_boolean);
create index index_066_04 on test_index_table_066(c_money,c_boolean,c_boolean);
create index index_066_05 on test_index_table_066(c_boolean,c_boolean,c_boolean);
create index index_066_06 on test_index_table_066(c_char,c_boolean,c_boolean);
create index index_066_07 on test_index_table_066(c_varchar,c_boolean,c_char);
create index index_066_08 on test_index_table_066(c_boolean,c_text,c_char);
create index index_066_09 on test_index_table_066(c_text,c_char,c_money);
create index index_066_10 on test_index_table_066(c_date,c_text,c_char);

select relname from pg_class where relname like 'index_066_%' order by relname;

--btree
drop index if exists index_066_01;
drop index if exists index_066_02;
drop index if exists index_066_03;
drop index if exists index_066_04;
drop index if exists index_066_05;
drop index if exists index_066_06;
drop index if exists index_066_07;
drop index if exists index_066_08;
drop index if exists index_066_09;
drop index if exists index_066_10;

create index index_066_01 on test_index_table_066 using btree(c_int,c_numeric,c_float);
create index index_066_02 on test_index_table_066 using btree(c_numeric,c_float,c_money);
create index index_066_03 on test_index_table_066 using btree(c_float,c_boolean,c_boolean);
create index index_066_04 on test_index_table_066 using btree(c_money,c_boolean,c_boolean);
create index index_066_05 on test_index_table_066 using btree(c_boolean,c_boolean,c_boolean);
create index index_066_06 on test_index_table_066 using btree(c_char,c_boolean,c_boolean);
create index index_066_07 on test_index_table_066 using btree(c_varchar,c_boolean,c_char);
create index index_066_08 on test_index_table_066 using btree(c_boolean,c_text,c_char);
create index index_066_09 on test_index_table_066 using btree(c_text,c_char,c_money);
create index index_066_10 on test_index_table_066 using btree(c_date,c_text,c_char);


select relname from pg_class where relname like 'index_066_%' order by relname;

--gin
drop index if exists index_066_01;
drop index if exists index_066_02;
drop index if exists index_066_03;
drop index if exists index_066_04;
drop index if exists index_066_05;
drop index if exists index_066_06;
drop index if exists index_066_07;
drop index if exists index_066_08;
drop index if exists index_066_09;
drop index if exists index_066_10;

create index index_066_01 on test_index_table_066 using gin(to_tsvector('english', c_int),to_tsvector('english', c_numeric),to_tsvector('english', c_float));
create index index_066_02 on test_index_table_066 using gin(to_tsvector('english', c_float),to_tsvector('english', c_varchar),to_tsvector('english', c_char));
create index index_066_03 on test_index_table_066 using gin(to_tsvector('english', c_clob),to_tsvector('english', c_numeric),to_tsvector('english', c_date));
create index index_066_06 on test_index_table_066 using gin(to_tsvector('english', c_int),to_tsvector('english', c_clob),to_tsvector('english', c_date));
create index index_066_07 on test_index_table_066 using gin(to_tsvector('english', c_clob),to_tsvector('english', c_numeric),to_tsvector('english', c_date));
create index index_066_08 on test_index_table_066 using gin(to_tsvector('english', c_date),to_tsvector('english', c_numeric),to_tsvector('english', c_float));

select relname from pg_class where relname like 'index_066_%' order by relname;
--清理环境
drop index if exists index_066_01;
drop index if exists index_066_02;
drop index if exists index_066_03;
drop index if exists index_066_04;
drop index if exists index_066_05;
drop index if exists index_066_06;
drop index if exists index_066_07;
drop index if exists index_066_08;
drop index if exists index_066_09;
drop index if exists index_066_10;
DROP TABLE if EXISTS test_index_table_066 CASCADE;