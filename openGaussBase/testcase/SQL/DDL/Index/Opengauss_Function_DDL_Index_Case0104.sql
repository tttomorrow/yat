--  @testpoint: where:where+聚集表达式：不支持
--Avg(),Count(),Max(),Min(),Sum()
DROP TABLE if EXISTS test_index_table_104 CASCADE;
create table test_index_table_104(
c_float1 float,
c_int int,
c_varchar varchar,
c_text text
) WITH (ORIENTATION = row) ;

begin
    for i in 0..1000 loop
       insert into test_index_table_104 values(i,i);
    end loop;
end;
/

--建索引
drop index if exists index_104_01;
create index index_104_01 on test_index_table_104(c_float1) where avg(c_int)>50;
create index index_104_01 on test_index_table_104(c_float1) where count(c_int)>50;
create index index_104_01 on test_index_table_104(c_float1) where max(c_int)>50;
create index index_104_01 on test_index_table_104(c_float1) where min(c_int)>50;
create index index_104_01 on test_index_table_104(c_float1) where sum(c_int)>50;
select relname from pg_class where relname like 'index_104_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_104 CASCADE;
