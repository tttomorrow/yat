--  @testpoint: REBUILD：设置gist索引不可用后重建

--建表
DROP TABLE if EXISTS test_index_table_137 CASCADE;
create table test_index_table_137(
c_point point
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_137 values(point(i,i));
    end loop;
end;
/

--建索引
drop index if exists index_137_01;
create index index_137_01 on test_index_table_137 using gist(c_point) ;
select relname from pg_class where relname like 'index_137_%' order by relname;

--UNUSABLE
--索引可被引用
explain select * from test_index_table_137 where c_point <^ point(50,50);
ALTER INDEX  index_137_01 UNUSABLE;
explain select * from test_index_table_137 where c_point <^ point(50,50);
--rebuild
ALTER INDEX index_137_01 REBUILD;
explain select * from test_index_table_137 where c_point <^ point(50,50);

--清理环境
DROP TABLE if EXISTS test_index_table_137 CASCADE;