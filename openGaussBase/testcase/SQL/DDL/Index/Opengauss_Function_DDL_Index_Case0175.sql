--  @testpoint:对表重命名查看索引

--建普通表
DROP TABLE if EXISTS test_index_table_175 CASCADE;
create table test_index_table_175(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_175_01;
create index index_175_01 on test_index_table_175(c_int) local (partition p1,partition p2,partition p3,partition p4);
select relname from pg_class where relname like 'index_175_%';
explain select c_int from test_index_table_175 where c_int > 5000 group by c_int;

--重命名
alter table test_index_table_175  rename to test_index_table_175_01;
explain select c_int from test_index_table_175_01 where c_int > 5000 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_175_01 CASCADE;