--  @testpoint:TABLESPACE：与表不在同一空间:success

--建表空间
drop tablespace if exists test_space_01;
CREATE TABLESPACE test_space_01 RELATIVE LOCATION 'tablespace/tablespace_1';
drop tablespace if exists test_space_02;
CREATE TABLESPACE test_space_02 RELATIVE LOCATION 'tablespace/tablespace_2';

DROP TABLE if EXISTS test_index_table_097 CASCADE;
create table test_index_table_097(
c_float1 float
) WITH (ORIENTATION = row) TABLESPACE test_space_01;

begin
    for i in 0..10000 loop
        insert into test_index_table_097 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_097_01;
create index index_097_01 on test_index_table_097 using btree(c_float1)  TABLESPACE test_space_02 where c_float1 >50;
select relname from pg_class where relname like 'index_097_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_097 CASCADE;
drop tablespace if exists test_space_01;
drop tablespace if exists test_space_02;
