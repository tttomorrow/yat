--  @testpoint: SET TABLESPACE：已设置表空间，设置为新的表空间

drop tablespace if exists test_space_119_01;
drop tablespace if exists test_space_119_02;
CREATE TABLESPACE test_space_119_01 RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE TABLESPACE test_space_119_02 RELATIVE LOCATION 'tablespace/tablespace_2';

DROP TABLE if EXISTS test_index_table_119 CASCADE;
create table test_index_table_119(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引
drop index if exists index_119_01;
create index index_119_01 on test_index_table_119(c_date) TABLESPACE test_space_119_01;
select relname from pg_class where relname like 'index_119_%' order by relname;

--set TABLESPACE

--select tablespace from pg_indexes where indexname = 'index_119_01';
select spcname from PG_TABLESPACE where oid = (select reltablespace from pg_class where relname ='index_119_01');
ALTER INDEX index_119_01  SET TABLESPACE test_space_119_02;
select spcname from PG_TABLESPACE where oid = (select reltablespace from pg_class where relname ='index_119_01');

--清理环境
DROP TABLE if EXISTS test_index_table_119 CASCADE;
drop tablespace if exists test_space_119_01;
drop tablespace if exists test_space_119_02;