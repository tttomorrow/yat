--  @testpoint: TABLESPACE index_partition_tablespace：不存在的分区表空间

drop tablespace if exists test_space_111_01;
CREATE TABLESPACE test_space_111_01 RELATIVE LOCATION 'tablespace/tablespace_1';
drop tablespace if exists test_space_111_01;

DROP TABLE if EXISTS test_index_table_111 CASCADE;
create table test_index_table_111(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引：合理报错
drop index if exists index_111_01;
create index index_111_01 on test_index_table_111(c_date) TABLESPACE test_space_111_01;
select relname from pg_class where relname like 'index_111_%' order by relname;

--清理数据
DROP TABLE if EXISTS test_index_table_111 CASCADE;
drop tablespace if exists test_space_111_01;
