--  @testpoint: where:引用表中所有列

DROP TABLE if EXISTS test_index_table_101 CASCADE;
create table test_index_table_101(
c_float1 float,
c_int int,
c_varchar varchar,
c_text text
) WITH (ORIENTATION = row) ;

begin
    for i in 0..1000 loop
        insert into test_index_table_101 values(i,i);
    end loop;
end;
/

--建索引
drop index if exists index_101_01;
create index index_101_01 on test_index_table_101 using btree(c_float1) where c_int >10 and c_varchar like '%1%' and c_text like '%1%';
select relname from pg_class where relname like 'index_101_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_101 CASCADE;