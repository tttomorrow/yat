--  @testpoint: UNUSABLE：行存表普通表+临时表设置索引不可用

--建普通表
DROP TABLE if EXISTS test_index_table_129 CASCADE;
create table test_index_table_129(
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_129 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_129_01;
create index index_129_01 on test_index_table_129(c_int) ;
select relname from pg_class where relname like 'index_129_%' order by relname;

--索引可被引用
explain select * from test_index_table_129 where c_int >50 group by c_int ;
ALTER INDEX  index_129_02 UNUSABLE;
ALTER INDEX  IF EXISTS  index_129_02 UNUSABLE;
ALTER INDEX  IF EXISTS  index_129_01 UNUSABLE;
--索引不被引用
explain select * from test_index_table_129 where c_int >50;

--建临时表
DROP TABLE if EXISTS test_index_table_129 CASCADE;
create temporary table test_index_table_129(
c_int int
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_129 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_129_01;
create index index_129_01 on test_index_table_129(c_int) ;
select relname from pg_class where relname like 'index_129_%' order by relname;

--索引可被引用
explain select * from test_index_table_129 where c_int >50 group by c_int ;
ALTER INDEX  index_129_02 UNUSABLE;
ALTER INDEX  IF EXISTS  index_129_02 UNUSABLE;
ALTER INDEX  IF EXISTS  index_129_01 UNUSABLE;
--索引不被引用
explain select * from test_index_table_129 where c_int >50 group by c_int ;

--清理环境
DROP TABLE if EXISTS test_index_table_129 CASCADE;