-- @testpoint: --唯一索引：行存表not null+唯一索引：success
--建表
DROP TABLE if EXISTS test_index_table_055_01 CASCADE;
DROP TABLE if EXISTS test_index_table_055_02 CASCADE;
DROP TABLE if EXISTS test_index_table_055_03 CASCADE;
create table test_index_table_055_01(id int check(id <> 0));
create table test_index_table_055_02(id int check(id <> 0)) WITH (ORIENTATION = row)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE));
create  TEMPORARY table test_index_table_055_03(id int check(id <> 0));

--建索引
DROP INDEX IF EXISTS index_055_01;
DROP INDEX IF EXISTS index_055_02;
DROP INDEX IF EXISTS index_055_03;
create unique index index_055_01 on test_index_table_055_01(id);
create unique index index_055_02 on test_index_table_055_02(id) local;
create unique index index_055_03 on test_index_table_055_03(id);

--查询索引
select relname from pg_class where relname='index_055_01';
select relname from pg_class where relname='index_055_02';
select relname from pg_class where relname='index_055_03';
explain select * from test_index_table_055_01 where id=1;
explain select * from test_index_table_055_02 where id=1;
explain select * from test_index_table_055_03 where id=1;

--清理数据
DROP TABLE if EXISTS test_index_table_055_01 CASCADE;
DROP TABLE if EXISTS test_index_table_055_02 CASCADE;
DROP TABLE if EXISTS test_index_table_055_03 CASCADE;