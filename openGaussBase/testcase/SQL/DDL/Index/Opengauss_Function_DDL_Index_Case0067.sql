--  @testpoint: column_name：列存分区表常用数据类型3列：合理报错
DROP TABLE if EXISTS test_index_table_067 CASCADE;
create table test_index_table_067(
c_int INTEGER,
c_float FLOAT,
c_varchar VARCHAR
) WITH (ORIENTATION = column) PARTITION BY RANGE(c_int)(PARTITION P1 VALUES LESS THAN(100));

--建psort索引：合理报错
drop index if exists index_067_01;

create index index_067_01 on test_index_table_067 using psort(c_int,c_float,c_varchar);
select relname from pg_class where relname like 'index_067_%' order by relname;

--btree：合理报错
drop index if exists index_067_01;

create index index_067_01 on test_index_table_067 using btree(c_int,c_varchar,c_float);
select relname from pg_class where relname like 'index_067_%' order by relname;

--gist：合理报错
drop index if exists index_067_01;

create index index_067_01 on test_index_table_067 using gist(c_int,c_varchar,c_float);
select relname from pg_class where relname like 'index_067_%' order by relname;

--gin：合理报错
drop index if exists index_067_01;

create index index_067_01 on test_index_table_067 using gin(to_tsvector('english', c_int),to_tsvector('english', c_varchar),to_tsvector('english', c_float));
select relname from pg_class where relname like 'index_067_%' order by relname;

--清理环境
drop index if exists index_067_01;
DROP TABLE if EXISTS test_index_table_067 CASCADE;