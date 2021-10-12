--  @testpoint: TABLESPACE：与表同一空间:success
--建表空间
drop tablespace if exists test_space;
CREATE TABLESPACE test_space RELATIVE LOCATION 'tablespace/tablespace_1';

DROP TABLE if EXISTS test_index_table_096 CASCADE;
create table test_index_table_096(
c_float1 float
) WITH (ORIENTATION = row) TABLESPACE test_space;

begin
    for i in 0..100000 loop
        insert into test_index_table_096 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_096_01;
create index index_096_01 on test_index_table_096 using btree(c_float1)  TABLESPACE test_space where c_float1 >50;
select relname from pg_class where relname like 'index_096_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_096 CASCADE;
drop tablespace if exists test_space;