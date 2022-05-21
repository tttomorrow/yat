-- @testpoint: REBUILD：自动拓展分区表设置索引不可用后重建

--建自动拓展分区表
DROP TABLE if EXISTS test_index_table_136 CASCADE;
create table test_index_table_136(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date) interval ('1 month')  (
partition p1 values less than ('1990-01-01 00:00:00')
);

begin
  for i in 1..30 loop
    insert into test_index_table_136 values(
    i,
    to_date('2020-08-01','yyyy-mm-dd' )+i
    );
  end loop;
end;
/

--建索引
drop index if exists index_136_01;
create index index_136_01 on test_index_table_136(c_int) local (PARTITION p1,PARTITION p2);
select relname from pg_class where relname like 'index_136_%' order by relname;

--UNUSABLE
--索引可被引用
explain select * from test_index_table_136 where c_int >10 group by c_int,c_date ;
--can not set unusable index partition against NON-PARTITIONED index
ALTER INDEX  index_136_01 modify PARTITION p2 UNUSABLE;
--索引不被引用
explain select * from test_index_table_136 where c_int >10 group by c_int,c_date ;
--rebuild
ALTER INDEX index_136_01 REBUILD  PARTITION p2;
explain select * from test_index_table_136 where c_int >10 group by c_int,c_date ;

--清理环境
DROP TABLE if EXISTS test_index_table_136 CASCADE;