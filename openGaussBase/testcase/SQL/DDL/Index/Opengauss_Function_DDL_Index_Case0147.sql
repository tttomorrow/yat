--  @testpoint: MOVE PARTITION：分区表未设置或已设置表空间，设置为不存在的表空间

drop tablespace if exists test_space_147_01;
drop tablespace if exists test_space_147_02;
CREATE TABLESPACE test_space_147_01 RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE TABLESPACE test_space_147_02 RELATIVE LOCATION 'tablespace/tablespace_2';
drop tablespace if exists test_space_147_02;


DROP TABLE if EXISTS test_index_table_147 CASCADE;
create table test_index_table_147(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00'),
partition p2 values less than ('2020-01-01 00:00:00')
);

--建索引
drop index if exists index_147_01;
drop index if exists index_147_02;
create index index_147_01 on test_index_table_147(c_date) local (PARTITION p1 ,PARTITION p2);
create index index_147_02 on test_index_table_147(c_date) local (PARTITION p1 TABLESPACE test_space_147_01,PARTITION p2 TABLESPACE test_space_147_01);
select relname from pg_class where relname like 'index_147_%' order by relname;

--MOVE PARTITION
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_147_01'));
ALTER INDEX index_147_01 MOVE PARTITION p1 TABLESPACE test_space_147_02;
ALTER INDEX index_147_01 MOVE PARTITION p2 TABLESPACE test_space_147_02;
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_147_01'));

select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_147_02'));
ALTER INDEX index_147_02 MOVE PARTITION p1 TABLESPACE test_space_147_02;
ALTER INDEX index_147_02 MOVE PARTITION p2 TABLESPACE test_space_147_02;
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_147_02'));

--清理环境
DROP TABLE if EXISTS test_index_table_147 CASCADE;
drop tablespace if exists test_space_147_01;