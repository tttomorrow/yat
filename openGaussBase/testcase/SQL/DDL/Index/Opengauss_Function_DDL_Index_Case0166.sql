-- @testpoint: 函数：索引的增删改

--建函数
drop procedure if exists fun_166;
create  function fun_166() return int
as
b int := 1;
begin
    DROP TABLE if EXISTS test_index_table_166 CASCADE;
    create table test_index_table_166(
    c_int int
    ) WITH (ORIENTATION = row) partition by range(c_int)(
    partition p1 values less than (100),
    partition p2 values less than (1000),
    partition p3 values less than (5000),
    partition p4 values less than (10001)
    );

    drop index if exists index_166_01;
    create index index_166_01 on test_index_table_166(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
    alter index index_166_01 rename to index_166_02;
    alter index index_166_02 MODIFY PARTITION p1 UNUSABLE;
    REINDEX table test_index_table_166;
    drop table test_index_table_166 cascade;
    return b;
end;
/

select fun_166();
drop procedure if exists fun_166;