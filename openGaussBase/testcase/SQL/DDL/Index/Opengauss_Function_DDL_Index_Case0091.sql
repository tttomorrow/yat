--  @testpoint: with：FILLFACTOR:0-100
--FILLFACTOR
--创建索引时，可以指定一个填充因子，以便在索引的每个叶级页上留出额外的间隙和保留一定百分比的空间，
--供将来表的数据存储容量进行扩充和减少页拆分的可能 性。填充因子的值是从   0   到   100   的百分比数值，
--指定在创建索引后对数据页的填充比例。值为   100   时表示页将填满，所留出的存储空间量最小。只有当不会对数据进行更改时（例如，在只读表中）才会使用此设置。
--值越小则数据页上的空闲空间越大，这样可以减 少在索引增长过程中对数据页进行拆分的需要，但需要更多的存储空间。当表中数据会发生更改时，这种设置更为适当

DROP TABLE if EXISTS test_index_table_091 CASCADE;
create table test_index_table_091(
c_float1 float
) WITH (ORIENTATION = row) ;

begin
    for i in 0..100000 loop
        insert into test_index_table_091 values(i);
    end loop;
end;
/

--建btree索引:fillfactor 100
drop index if exists index_091_01;
create index index_091_01 on test_index_table_091 using btree(c_float1) with (fillfactor=100) where  c_float1 > 50 ;
select relname from pg_class where relname like 'index_091_%' order by relname;
--索引有效
explain select * from test_index_table_091 where c_float1 >50 group by c_float1;

--建btree索引:fillfactor 99
drop index if exists index_091_01;
create index index_091_01 on test_index_table_091 using btree(c_float1) with (fillfactor=99) where  c_float1 > 50 ;
select relname from pg_class where relname like 'index_091_%' order by relname;
--索引有效
explain select * from test_index_table_091 where c_float1 >50 group by c_float1;
--填充因子低 查询效率低，索引不被调用
--建btree索引:fillfactor 11
drop index if exists index_091_01;
create index index_091_01 on test_index_table_091 using btree(c_float1) with (fillfactor=11) where  c_float1 > 50 ;
select relname from pg_class where relname like 'index_091_%' order by relname;
--索引不被调用
explain select * from test_index_table_091 where c_float1 >50 group by c_float1;

--建btree索引:fillfactor 10
drop index if exists index_091_01;
create index index_091_01 on test_index_table_091 using btree(c_float1) with (fillfactor=10) where  c_float1 > 50 ;
select relname from pg_class where relname like 'index_091_%' order by relname;
--索引不被调用
explain select * from test_index_table_091 where c_float1 >50 group by c_float1;


--清理环境
DROP TABLE if EXISTS test_index_table_091 CASCADE;