--  @testpoint: create index CONCURRENTLY：在事务中进行：合理报错

--建普通表
DROP TABLE if EXISTS test_index_table_192 CASCADE;
create table test_index_table_192(
c_int int);

--建索引
drop index if exists index_192_01;
begin
    create index CONCURRENTLY index_192_01 on test_index_table_192(c_int);
end;
/

--清理环境
DROP TABLE if EXISTS test_index_table_192 CASCADE;