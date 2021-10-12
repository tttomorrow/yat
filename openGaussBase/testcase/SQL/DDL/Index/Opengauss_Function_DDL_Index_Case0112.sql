--  @testpoint: DCL+DML调用索引
--创建表
DROP TABLE if EXISTS test_index_table_112_01 CASCADE;
create table test_index_table_112_01(
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_112_01 values(i);
    end loop;
end;
/
--创建表
DROP TABLE if EXISTS test_index_table_112_02 CASCADE;
create table test_index_table_112_02(
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_112_02 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_112_01;
create index index_112_01 on test_index_table_112_01(c_int);
select relname from pg_class where relname like 'index_112_%' order by relname;

--调用索引
explain select distinct c_int from test_index_table_112_01 where c_int >5 group by c_int;
explain analyze select * from test_index_table_112_01 a join  test_index_table_112_02  b on a.c_int=b.c_int where a.c_int > 500 group by a.c_int,b.c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_112_01 CASCADE;
DROP TABLE if EXISTS test_index_table_112_02 CASCADE;