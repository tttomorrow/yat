-- @testpoint: 排序：NULLS FIRST
--指定空值在排序中排在非空值之前，当指定DESC排序时，本选项为默认的。
DROP TABLE if EXISTS test_index_table_089 CASCADE;
create table test_index_table_089(
c_float1 float
) WITH (ORIENTATION = row) ;
insert into test_index_table_089 values(null);
insert into test_index_table_089 values('');
begin
    for i in 0..10000 loop
        insert into test_index_table_089 values(i);
    end loop;
end;
/

--建btree索引:5-5
drop index if exists index_089_01;
create index index_089_01 on test_index_table_089 using btree(c_float1 desc NULLS  FIRST );
select relname from pg_class where relname like 'index_089_%' order by relname;
--索引有效
explain select * from test_index_table_089 where c_float1 >0 order by c_float1 desc limit 10;
--空值排序在非空值之前
select * from test_index_table_089 order by c_float1 desc limit 10;
--清理环境
DROP TABLE if EXISTS test_index_table_089 CASCADE;