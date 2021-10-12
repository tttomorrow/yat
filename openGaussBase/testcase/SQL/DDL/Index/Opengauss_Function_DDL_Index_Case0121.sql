--  @testpoint: SET TABLESPACE：未设置表空间，设置为新的表空间

drop tablespace if exists test_space_121_01;
CREATE TABLESPACE test_space_121_01 RELATIVE LOCATION 'tablespace/tablespace_1';


DROP TABLE if EXISTS test_index_table_121 CASCADE;
create table test_index_table_121(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引
drop index if exists index_121_01;
create index index_121_01 on test_index_table_121(c_date);
select relname from pg_class where relname like 'index_121_%' order by relname;

--set TABLESPACE
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_121_01'));

ALTER INDEX index_121_01  SET TABLESPACE test_space_121_01;

select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_121_01'));

--清理环境
DROP TABLE if EXISTS test_index_table_121 CASCADE;
drop tablespace if exists test_space_121_01;
