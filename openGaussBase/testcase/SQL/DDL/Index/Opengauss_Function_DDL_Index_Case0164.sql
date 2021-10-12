-- @testpoint:  reindex table：分区表设置索引不可用重建表

--建普通表
DROP TABLE if EXISTS test_index_table_164 CASCADE;
create table test_index_table_164(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

begin
    for i in 0..10000 loop
        insert into test_index_table_164 values(i);
    end loop;
end;
/

--建local索引
drop index if exists index_164_01;
create index index_164_01 on test_index_table_164(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_164_%' order by relname;
explain select * from test_index_table_164 where c_int > 5 group by c_int;
explain select * from test_index_table_164 where c_int > 500 group by c_int;
explain select * from test_index_table_164 where c_int > 2000 group by c_int;
explain select * from test_index_table_164 where c_int > 5000 group by c_int;

--reindex
alter index index_164_01 MODIFY PARTITION p1 UNUSABLE;
explain select * from test_index_table_164 where c_int > 5 group by c_int;
alter index index_164_01 MODIFY PARTITION p2 UNUSABLE;
explain select * from test_index_table_164 where c_int > 500 group by c_int;
alter index index_164_01 MODIFY PARTITION p3 UNUSABLE;
explain select * from test_index_table_164 where c_int > 2000 group by c_int;
alter index index_164_01 MODIFY PARTITION p4 UNUSABLE;
explain select * from test_index_table_164 where c_int > 5000 group by c_int;

REINDEX table test_index_table_164;
explain select * from test_index_table_164 where c_int > 5 group by c_int;
explain select * from test_index_table_164 where c_int > 500 group by c_int;
explain select * from test_index_table_164 where c_int > 2000 group by c_int;
explain select * from test_index_table_164 where c_int > 5000 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_164 CASCADE;