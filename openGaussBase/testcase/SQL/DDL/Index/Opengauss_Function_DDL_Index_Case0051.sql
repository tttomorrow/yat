--  @testpoint: 唯一索引：唯一约束+唯一索引：success
--建表
DROP TABLE if EXISTS test_index_table_051_01 CASCADE;
DROP TABLE if EXISTS test_index_table_051_02 CASCADE;
DROP TABLE if EXISTS test_index_table_051_03 CASCADE;
create table test_index_table_051_01(id int unique);
create table test_index_table_051_02(id int unique) WITH (ORIENTATION = row)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
create  TEMPORARY table test_index_table_051_03(id int unique);

--建索引
DROP INDEX IF EXISTS index_051_01;
DROP INDEX IF EXISTS index_051_02;
DROP INDEX IF EXISTS index_051_03;
create unique index index_051_01 on test_index_table_051_01(id);
create unique index index_051_02 on test_index_table_051_02(id) local;
create unique index index_051_03 on test_index_table_051_03(id);

--查询索引
select relname from pg_class where relname='index_051_01';
select relname from pg_class where relname='index_051_02';
select relname from pg_class where relname='index_051_03';

--清理数据
DROP TABLE if EXISTS test_index_table_051_01 CASCADE;
DROP TABLE if EXISTS test_index_table_051_02 CASCADE;
DROP TABLE if EXISTS test_index_table_051_03 CASCADE;