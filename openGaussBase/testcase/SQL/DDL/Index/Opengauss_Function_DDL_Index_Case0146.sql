--  @testpoint: MOVE PARTITION：分区表未设置表空间，设置为新的表空间

drop tablespace if exists test_space_146_01;
CREATE TABLESPACE test_space_146_01 RELATIVE LOCATION 'tablespace/tablespace_1';

DROP TABLE if EXISTS test_index_table_146 CASCADE;
create table test_index_table_146(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00'),
partition p2 values less than ('2020-01-01 00:00:00')
);

--建索引
drop index if exists index_146_01;
create index index_146_01 on test_index_table_146(c_date) local (PARTITION p1 ,PARTITION p2);
select relname from pg_class where relname like 'index_146_%' order by relname;

--MOVE PARTITION
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_146_01'));
ALTER INDEX index_146_01 MOVE PARTITION p1 TABLESPACE test_space_146_01;
ALTER INDEX index_146_01 MOVE PARTITION p2 TABLESPACE test_space_146_01;
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_146_01'));

--清理环境
DROP TABLE if EXISTS test_index_table_146 CASCADE;
drop tablespace if exists test_space_146_01;