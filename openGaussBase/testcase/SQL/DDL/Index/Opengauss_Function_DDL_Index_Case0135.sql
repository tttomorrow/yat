--  @testpoint: REBUILD：分区表普通表设置索引不可用后重建

--建普通表
DROP TABLE if EXISTS test_index_table_135 CASCADE;
create table test_index_table_135(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

begin
    for i in 0..10000 loop
        insert into test_index_table_135 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_135_01;
create index index_135_01 on test_index_table_135(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_135_%' order by relname;

--UNUSABLE
--索引可被引用
explain select * from test_index_table_135 where c_int >50 group by c_int ;
--can not set unusable index partition against NON-PARTITIONED index
ALTER INDEX  index_135_01 modify PARTITION p2 UNUSABLE;
--索引不被引用
explain select * from test_index_table_135 where c_int >50 group by c_int ;
--rebuild
ALTER INDEX index_135_01 REBUILD  PARTITION p2;
explain select * from test_index_table_135 where c_int >50 group by c_int ;

--清理环境
DROP TABLE if EXISTS test_index_table_135 CASCADE;