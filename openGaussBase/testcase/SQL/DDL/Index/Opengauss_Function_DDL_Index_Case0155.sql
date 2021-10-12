--  @testpoint: DROP CASCADE:各索引类型+表

--建分区表
DROP TABLE if EXISTS test_index_table_155_01 CASCADE;
create table test_index_table_155_01(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建分区表
DROP TABLE if EXISTS test_index_table_155_02 CASCADE;
create table test_index_table_155_02(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引
create unique index index_155_01 on test_index_table_155_01(c_int);
create unique index index_155_02 on test_index_table_155_02(c_int);
select indexname from pg_indexes where tablename like '%test_index_table_155%' order by indexname asc;

--添加外键约束
alter table test_index_table_155_02 add constraint fk_01_cint foreign key (c_int) references test_index_table_155_01(c_int);
select conname from PG_CONSTRAINT where conrelid = (select oid from pg_class where relname='test_index_table_155_02');

--drop cascade
drop index  index_155_01 cascade;
select indexname from pg_indexes where tablename like '%test_index_table_155%' order by indexname asc;
select conname from PG_CONSTRAINT where conrelid = (select oid from pg_class where relname='test_index_table_155_02');


--建普通表
DROP TABLE if EXISTS test_index_table_155_01 CASCADE;
create table test_index_table_155_01(
c_int int);

--建普通表
DROP TABLE if EXISTS test_index_table_155_02 CASCADE;
create table test_index_table_155_02(
c_int int);

--建索引
create unique index index_155_01 on test_index_table_155_01(c_int);
create unique index index_155_02 on test_index_table_155_02(c_int);
select relname from pg_class where relname like 'index_155_%' order by relname;

--添加外键约束
alter table test_index_table_155_02 add constraint fk_01_cint foreign key (c_int) references test_index_table_155_01(c_int);
select conname from PG_CONSTRAINT where conrelid = (select oid from pg_class where relname='test_index_table_155_02');

--drop cascade
drop index  index_155_01 cascade;
select relname from pg_class where relname like 'index_155_%' order by relname;
select conname from PG_CONSTRAINT where conrelid = (select oid from pg_class where relname='test_index_table_155_02');

--建临时表
DROP TABLE if EXISTS test_index_table_155_01 CASCADE;
create temporary table test_index_table_155_01(
c_int int);

--建临时表
DROP TABLE if EXISTS test_index_table_155_02 CASCADE;
create temporary table test_index_table_155_02(
c_int int);

--建索引
create unique index index_155_01 on test_index_table_155_01(c_int);
create unique index index_155_02 on test_index_table_155_02(c_int);
select relname from pg_class where relname like 'index_155_%' order by relname;

--添加外键约束
alter table test_index_table_155_02 add constraint fk_01_cint foreign key (c_int) references test_index_table_155_01(c_int);
select conname from PG_CONSTRAINT where conrelid = (select oid from pg_class where relname='test_index_table_155_02');

--drop cascade
drop index  index_155_01 cascade;
select relname from pg_class where relname like 'index_155_%' order by relname;
select conname from PG_CONSTRAINT where conrelid = (select oid from pg_class where relname='test_index_table_155_02');

--列存不支持外键
--psort不支持unique
--gist不支持unique

--清理环境
DROP TABLE if EXISTS test_index_table_155_01 CASCADE;
DROP TABLE if EXISTS test_index_table_155_02 CASCADE;
