--  @testpoint:where:引用表中未被索引的列

DROP TABLE if EXISTS test_index_table_100 CASCADE;
create table test_index_table_100(
c_float1 float,
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..100000 loop
        insert into test_index_table_100 values(i,i);
    end loop;
end;
/

--建索引
drop index if exists index_100_01;
create index index_100_01 on test_index_table_100 using btree(c_float1) where c_int >10;
select relname from pg_class where relname like 'index_100_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_100 CASCADE;