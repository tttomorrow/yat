--  @testpoint: expression：包含is null子句
--行存表
DROP TABLE if EXISTS test_index_table_083 CASCADE;
create table test_index_table_083(
c_float1 float
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_083 values(i);
    end loop;
end;
/

--建btree索引:不包含is null
drop index if exists index_083_01;
create index index_083_01 on test_index_table_083 using btree(c_float1) where c_float1 >0;
select relname from pg_class where relname like 'index_083_%' order by relname;
--索引有效
explain select * from test_index_table_083 where c_float1 >500 group by c_float1;
--建btree索引:包含is null
drop index if exists index_083_01;
create index index_083_01 on test_index_table_083 using btree(c_float1) where c_float1 is null;
select relname from pg_class where relname like 'index_083_%' order by relname;
--索引无效
explain select * from test_index_table_083 where c_float1 >500 group by c_float1;


--清理环境
DROP TABLE if EXISTS test_index_table_083 CASCADE;