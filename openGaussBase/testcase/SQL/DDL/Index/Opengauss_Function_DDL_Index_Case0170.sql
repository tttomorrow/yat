-- @testpoint:  reindex：schema

drop schema if exists index170 cascade;
create schema index170;
--建普通表
DROP TABLE if EXISTS index170.test_index_table_170 CASCADE;
create table index170.test_index_table_170(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

begin
    for i in 0..10000 loop
        insert into index170.test_index_table_170 values(i);
    end loop;
end;
/


--建local索引
drop index if exists index170.index_170_01;
create index index170.index_170_01 on index170.test_index_table_170(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_170_%' order by relname;
explain select * from index170.test_index_table_170 where c_int > 5000 group by c_int;

--reindex
alter index index170.index_170_01 UNUSABLE;
explain select * from index170.test_index_table_170 where c_int > 500 group by c_int;
REINDEX INDEX  index170.index_170_01;
explain select * from index170.test_index_table_170 where c_int > 500 group by c_int;
alter index index170.index_170_01 UNUSABLE;
explain select * from index170.test_index_table_170 where c_int > 500 group by c_int;
REINDEX table  index170.test_index_table_170;
explain select * from index170.test_index_table_170 where c_int > 500 group by c_int;

--清理环境
DROP TABLE if EXISTS index170.test_index_table_170 CASCADE;
drop schema if exists index170 cascade;