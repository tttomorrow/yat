--  @testpoint: TABLESPACE index_partition_tablespace：指定分区非分区表空间

drop tablespace if exists test_space_108_01;
drop tablespace if exists test_space_108_02;
CREATE TABLESPACE test_space_108_01 RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE TABLESPACE test_space_108_02 RELATIVE LOCATION 'tablespace/tablespace_2';

DROP TABLE if EXISTS test_index_table_108 CASCADE;
create table test_index_table_108(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00') TABLESPACE test_space_108_01
);

--建索引
drop index if exists index_108_01;
create index index_108_01 on test_index_table_108(c_date) TABLESPACE test_space_108_02;
select relname from pg_class where relname like 'index_108_%' order by relname;

DROP TABLE if EXISTS test_index_table_108 CASCADE;
create table test_index_table_108(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)  interval ('1 month')  (
partition p1 values less than ('1990-01-01 00:00:00') TABLESPACE test_space_108_01
);

--建索索引
drop index if exists index_108_01;
create index index_108_01 on test_index_table_108(c_date) TABLESPACE test_space_108_02;
select relname from pg_class where relname like 'index_108_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_108 CASCADE;
drop tablespace if exists test_space_108_01;
drop tablespace if exists test_space_108_02;