-- @testpoint: where:where+子查询：不支持 合理报错

DROP TABLE if EXISTS test_index_table_103 CASCADE;
create table test_index_table_103(
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

DROP TABLE if EXISTS test_index_table_103_02 CASCADE;
create table test_index_table_103_02(
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
drop index if exists index_103_01;
create index index_103_01 on test_index_table_103(c_float1) where c_int in (select c_int from test_index_table_103_02 where c_int>2) ;
select relname from pg_class where relname like 'index_103_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_103 CASCADE;
DROP TABLE if EXISTS test_index_table_103_02 CASCADE;