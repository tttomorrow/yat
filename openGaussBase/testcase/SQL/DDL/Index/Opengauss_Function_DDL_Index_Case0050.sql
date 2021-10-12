-- @testpoint: 唯一索引：合理报错 列存表psort+gin+btree不支持：普通表，分区表，临时表
--建表
DROP TABLE if EXISTS test_index_table_050_01 CASCADE;
DROP TABLE if EXISTS test_index_table_050_02 CASCADE;
DROP TABLE if EXISTS test_index_table_050_03 CASCADE;
create table test_index_table_050_01(id int) WITH (ORIENTATION = column);
create table test_index_table_050_02(id int) WITH (ORIENTATION = column)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE));
create  TEMPORARY table test_index_table_050_03(id int) WITH (ORIENTATION = column);

--建索引--临时表
DROP INDEX IF EXISTS index_050_01;
DROP INDEX IF EXISTS index_050_02;
DROP INDEX IF EXISTS index_050_03;
create unique index index_050_01 on test_index_table_050_03(id);
create unique index index_050_02 on test_index_table_050_03 USING gin(to_tsvector('english', id));
create unique index index_050_03 on test_index_table_050_03 USING btree(id) ;

--建索引--普通表
DROP INDEX IF EXISTS index_050_01;
DROP INDEX IF EXISTS index_050_02;
DROP INDEX IF EXISTS index_050_03;

create unique index index_050_01 on test_index_table_050_01(id);
create unique index index_050_02 on test_index_table_050_01 USING gin(to_tsvector('english', id));
create unique index index_050_03 on test_index_table_050_01 USING btree(id);

--建索引--分区表
DROP INDEX IF EXISTS index_050_01;
DROP INDEX IF EXISTS index_050_02;
DROP INDEX IF EXISTS index_050_03;
create unique index index_050_01 on test_index_table_050_02(id) local;
create unique index index_050_02 on test_index_table_050_02 USING gin(to_tsvector('english', id)) local;
create unique index index_050_03 on test_index_table_050_02 USING btree(id) local;


--清理数据
DROP INDEX IF EXISTS index_050_01;
DROP INDEX IF EXISTS index_050_02;
DROP INDEX IF EXISTS index_050_03;
DROP TABLE if EXISTS test_index_table_050_01 CASCADE;
DROP TABLE if EXISTS test_index_table_050_02 CASCADE;
DROP TABLE if EXISTS test_index_table_050_03 CASCADE;