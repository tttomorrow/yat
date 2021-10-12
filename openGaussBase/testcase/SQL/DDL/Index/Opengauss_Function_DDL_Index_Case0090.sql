-- @testpoint: 排序：NULLS LAST
--指定空值在排序中排在非空值之后，未指定DESC排序时，本选项为默认的。
DROP TABLE if EXISTS test_index_table_090 CASCADE;
create table test_index_table_090(
c_float1 float
) WITH (ORIENTATION = row) ;
insert into test_index_table_090 values(null);
insert into test_index_table_090 values('');
begin
    for i in 0..100 loop
        insert into test_index_table_090 values(i);
    end loop;
end;
/

--建btree索引:5-5
drop index if exists index_090_01;
create index index_090_01 on test_index_table_090 using btree(c_float1 asc NULLS LAST );
select relname from pg_class where relname like 'index_090_%' order by relname;
--索引有效
explain select * from test_index_table_090 where c_float1 >0 group by c_float1 limit 10;
--空值排序在非空值之前
select * from test_index_table_090 order by c_float1 limit 99,4;
--清理环境
DROP TABLE if EXISTS test_index_table_090 CASCADE;