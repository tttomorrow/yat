--  @testpoint:SET TABLESPACE：未设置或已设置表空间，设置为不存在的表空间

drop tablespace if exists test_space_122_01;
drop tablespace if exists test_space_122_02;

CREATE TABLESPACE test_space_122_01 RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE TABLESPACE test_space_122_02 RELATIVE LOCATION 'tablespace/tablespace_2';
drop tablespace if exists test_space_122_02;

DROP TABLE if EXISTS test_index_table_122 CASCADE;
create table test_index_table_122(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引
drop index if exists index_122_01;
drop index if exists index_122_02;
create index index_122_01 on test_index_table_122(c_date) TABLESPACE test_space_122_01;
create index index_122_02 on test_index_table_122(c_date);
select relname from pg_class where relname like 'index_122_%' order by relname;

--rename
select spcname from PG_TABLESPACE where oid in (select reltablespace from pg_class where relname like '%index_122%');
ALTER INDEX index_122_01  SET TABLESPACE test_space_122_02;
ALTER INDEX index_122_01  SET TABLESPACE test_space_122_02;
select spcname from PG_TABLESPACE where oid in (select reltablespace from pg_class where relname like '%index_122%');

--清理环境
DROP TABLE if EXISTS test_index_table_122 CASCADE;
drop tablespace if exists test_space_122_01;
drop tablespace if exists test_space_122_02;