--  @testpoint: DROP INDEX 在事务内执行

--建普通表
DROP TABLE if EXISTS test_index_table_154 CASCADE;
create table test_index_table_154(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引
drop index if exists index_154_01;
create index index_154_01 on test_index_table_154(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_154_%' order by relname;

--DROP
begin
    DROP INDEX index_154_01;
end;
/
select relname from pg_class where relname like 'index_154_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_154 CASCADE;