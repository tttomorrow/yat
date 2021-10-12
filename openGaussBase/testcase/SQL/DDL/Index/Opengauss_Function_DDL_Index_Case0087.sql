-- @testpoint: 排序：asc
DROP TABLE if EXISTS test_index_table_087 CASCADE;
create table test_index_table_087(
c_float1 float
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_087 values(i);
    end loop;
end;
/

--建btree索引
drop index if exists index_087_01;
create index index_087_01 on test_index_table_087 using btree(c_float1 asc);
select relname from pg_class where relname like 'index_087_%' order by relname;
--索引有效
explain select * from test_index_table_087 where c_float1 >500 group by c_float1 limit 10;

--清理环境
DROP TABLE if EXISTS test_index_table_087 CASCADE;