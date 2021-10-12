-- @testpoint: 唯一索引：行存表null约束+唯一索引：success
--建表
DROP TABLE if EXISTS test_index_table_052_01 CASCADE;
DROP TABLE if EXISTS test_index_table_052_02 CASCADE;
DROP TABLE if EXISTS test_index_table_052_03 CASCADE;
create table test_index_table_052_01(id int null);
create table test_index_table_052_02(id int null) WITH (ORIENTATION = row)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
create  TEMPORARY table test_index_table_052_03(id int null);

--建索引
DROP INDEX IF EXISTS index_052_01;
DROP INDEX IF EXISTS index_052_02;
DROP INDEX IF EXISTS index_052_03;
create unique index index_052_01 on test_index_table_052_01(id);
create unique index index_052_02 on test_index_table_052_02(id) local;
create unique index index_052_03 on test_index_table_052_03(id);

--查询索引
select relname from pg_class where relname='index_052_01';
select relname from pg_class where relname='index_052_02';
select relname from pg_class where relname='index_052_03';
explain select * from test_index_table_052_01 where id=1;
explain select * from test_index_table_052_02 where id=1;
explain select * from test_index_table_052_03 where id=1;

--清理数据
DROP TABLE if EXISTS test_index_table_052_01 CASCADE;
DROP TABLE if EXISTS test_index_table_052_02 CASCADE;
DROP TABLE if EXISTS test_index_table_052_03 CASCADE;