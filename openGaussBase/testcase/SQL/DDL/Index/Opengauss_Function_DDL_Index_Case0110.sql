--  @testpoint:PARTITION:index_partition_name自动拓展分区表

--分区表
drop tablespace if exists test_space_110_01;
drop tablespace if exists test_space_110_02;
CREATE TABLESPACE test_space_110_01 RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE TABLESPACE test_space_110_02 RELATIVE LOCATION 'tablespace/tablespace_2';

DROP TABLE if EXISTS test_index_table_110 CASCADE;
create table test_index_table_110(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date) interval ('1 day')  (
partition p1 values less than ('1990-01-01 00:00:00') TABLESPACE test_space_110_01
);

--建索引
drop index if exists index_110_01;
create index index_110_01 on test_index_table_110(c_date) local (PARTITION  p1 TABLESPACE test_space_110_01);
select relname from pg_class where relname like 'index_110_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_110 CASCADE;
drop tablespace if exists test_space_110_01;
drop tablespace if exists test_space_110_02;