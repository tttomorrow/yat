--  @testpoint: REBUILD：行存表普通表+临时表设置索引不可用后重建

--建普通表
DROP TABLE if EXISTS test_index_table_134 CASCADE;
create table test_index_table_134(
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_134 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_134_01;
create index index_134_01 on test_index_table_134(c_int) ;
select relname from pg_class where relname like 'index_134_%' order by relname;

--索引可被引用
explain select * from test_index_table_134 where c_int >50 group by c_int ;
ALTER INDEX  IF EXISTS  index_134_01 UNUSABLE;
--索引不被引用
explain select * from test_index_table_134 where c_int >50;
--REBUILD
ALTER INDEX index_134_01 REBUILD;
explain select * from test_index_table_134 where c_int >50;


--建临时表
DROP TABLE if EXISTS test_index_table_134 CASCADE;
create temporary table test_index_table_134(
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_134 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_134_01;
create index index_134_01 on test_index_table_134(c_int) ;
select relname from pg_class where relname like 'index_134_%' order by relname;

--索引可被引用
explain select * from test_index_table_134 where c_int >50 group by c_int ;
ALTER INDEX  IF EXISTS  index_134_01 UNUSABLE;
--索引不被引用
explain select * from test_index_table_134 where c_int >50 group by c_int ;
--REBUILD
ALTER INDEX index_134_01 REBUILD;
explain select * from test_index_table_134 where c_int >50;

--清理环境
DROP TABLE if EXISTS test_index_table_134 CASCADE;