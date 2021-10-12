-- @testpoint: 合理报错唯一索引：行存表B-tree索引支持：普通表，分区表，临时表：success:插入操作
--建表
DROP TABLE if EXISTS test_index_table_048_01 CASCADE;
DROP TABLE if EXISTS test_index_table_048_02 CASCADE;
DROP TABLE if EXISTS test_index_table_048_03 CASCADE;
create table test_index_table_048_01(id int);
create table test_index_table_048_02(id int) WITH (ORIENTATION = row)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
create  TEMPORARY table test_index_table_048_03(id int);

--建索引
create unique index index_048_01 on test_index_table_048_01(id);
create unique index index_048_02 on test_index_table_048_02(id) local;
create unique index index_048_03 on test_index_table_048_03(id);

--查询索引
select relname from pg_class where relname='index_048_01';
select relname from pg_class where relname='index_048_02';
select relname from pg_class where relname='index_048_03';

--插入数据检查唯一索引是否生效
insert into test_index_table_048_01 values(1),(2),(1);
insert into test_index_table_048_02 values(1),(2),(1);
insert into test_index_table_048_03 values(1),(2),(1);

--清理数据
DROP TABLE if EXISTS test_index_table_048_01 CASCADE;
DROP TABLE if EXISTS test_index_table_048_02 CASCADE;
DROP TABLE if EXISTS test_index_table_048_03 CASCADE;