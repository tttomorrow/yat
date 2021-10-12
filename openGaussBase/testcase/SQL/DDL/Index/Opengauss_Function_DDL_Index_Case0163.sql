-- @testpoint: truncate之后做reindex

--建普通表
DROP TABLE if EXISTS test_index_table_163 CASCADE;
create table test_index_table_163(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

begin
    for i in 0..10000 loop
        insert into test_index_table_163 values(i);
    end loop;
end;
/

--建local索引
drop index if exists index_163_01;
create index index_163_01 on test_index_table_163(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_163_%' order by relname;
explain select * from test_index_table_163 where c_int > 500 group by c_int;

--reindex
alter index index_163_01 MODIFY PARTITION p2 UNUSABLE;
explain select * from test_index_table_163 where c_int > 500 group by c_int;
truncate test_index_table_163;
REINDEX table test_index_table_163 PARTITION p2;
explain select * from test_index_table_163 where c_int > 500 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_163 CASCADE;