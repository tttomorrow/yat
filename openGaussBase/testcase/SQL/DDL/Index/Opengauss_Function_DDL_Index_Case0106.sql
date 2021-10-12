--  @testpoint: PARTITION:global和local
--行存
DROP TABLE if EXISTS test_index_table_106 CASCADE;
create table test_index_table_106(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引同一列建本地和全局索引：合理报错
drop index if exists index_106_01;
create index index_106_01 on test_index_table_106(c_date) local;
create index index_106_01 on test_index_table_106(c_date) global;
select relname from pg_class where relname like 'index_106_%' order by relname;

DROP TABLE if EXISTS test_index_table_106 CASCADE;
create table test_index_table_106(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date) interval ('10 day') (
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引
drop index if exists index_106_01;
create index index_106_01 on test_index_table_106(c_date) local;
create index index_106_01 on test_index_table_106(c_date) global;
select relname from pg_class where relname like 'index_106_%' order by relname;

--列存
DROP TABLE if EXISTS test_index_table_106 CASCADE;
create table test_index_table_106(
c_int int,
c_date date
) WITH (ORIENTATION = column) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引：合理报错
drop index if exists index_106_01;
create index index_106_01 on test_index_table_106(c_date) local;
create index index_106_01 on test_index_table_106(c_date) global;
select relname from pg_class where relname like 'index_106_%' order by relname;

DROP TABLE if EXISTS test_index_table_106 CASCADE;
create table test_index_table_106(
c_int int,
c_date date
) WITH (ORIENTATION = column) partition by range(c_date) interval ('10 day') (
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引同一列建本地和全局索引：合理报错
drop index if exists index_106_01;
create index index_106_01 on test_index_table_106(c_date) local;
create index index_106_01 on test_index_table_106(c_date) global;
select relname from pg_class where relname like 'index_106_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_106 CASCADE;