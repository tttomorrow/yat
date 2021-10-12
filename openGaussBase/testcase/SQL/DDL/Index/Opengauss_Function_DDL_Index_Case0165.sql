-- @testpoint: 存储过程：索引的增删改

--建存储过程
drop procedure if exists PEOC_165;
create or replace procedure PEOC_165()
as
begin
    DROP TABLE if EXISTS test_index_table_165 CASCADE;
    create table test_index_table_165(
    c_int int
    ) WITH (ORIENTATION = row) partition by range(c_int)(
    partition p1 values less than (100),
    partition p2 values less than (1000),
    partition p3 values less than (5000),
    partition p4 values less than (10001)
    );

    drop index if exists index_165_01;
    create index index_165_01 on test_index_table_165(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
    alter index index_165_01 rename to index_165_02;
    alter index index_165_02 MODIFY PARTITION p1 UNUSABLE;
    REINDEX table test_index_table_165;
    drop table test_index_table_165 cascade;
end;
/

call PEOC_165();
drop procedure if exists PEOC_165;