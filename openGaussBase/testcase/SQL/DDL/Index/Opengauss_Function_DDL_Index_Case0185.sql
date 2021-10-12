-- @testpoint: create index与insert结合：先插入数据，再建索引，再插入数据，再删除数据，再重建索引

--建普通表
DROP TABLE if EXISTS test_index_table_185 CASCADE;
create table test_index_table_185(
c_int int);
--插入数据
begin
    for i in 0..30000 loop
        insert into test_index_table_185 values(i);
    end loop;
end;
/
--建索引
explain select * from test_index_table_185 where c_int >= 50 group by c_int;
drop index if exists index_185_01;
create index index_185_01 on test_index_table_185(c_int);
select relname from pg_class where relname like 'index_185_%';
explain select * from test_index_table_185 where c_int >= 50 group by c_int;

--插入数据
begin
    for i in 30000..60000 loop
        insert into test_index_table_185 values(i);
    end loop;
end;
/
--删除数据后重建索引
explain select * from test_index_table_185 where c_int >= 50 group by c_int;
delete from test_index_table_185;
explain select * from test_index_table_185 where c_int >= 50 group by c_int;
ALTER INDEX index_185_01 REBUILD;
explain select * from test_index_table_185 where c_int >= 50 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_185_01 CASCADE;
DROP TABLE if EXISTS test_index_table_185 CASCADE;