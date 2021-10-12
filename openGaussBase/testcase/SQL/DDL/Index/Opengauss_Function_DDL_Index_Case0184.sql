--  @testpoint:if not exists创建索引：合理报错

--建普通表
DROP TABLE if EXISTS test_index_table_184 CASCADE;
create table test_index_table_184(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_184_01;
select relname from pg_class where relname like 'index_184_%';
create index IF NOT EXISTS index_184_01 on test_index_table_184(c_int) local (partition p1,partition p2,partition p3,partition p4);
select relname from pg_class where relname like 'index_184_%';
explain select * from test_index_table_184 where c_int >= 50 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_184 CASCADE;