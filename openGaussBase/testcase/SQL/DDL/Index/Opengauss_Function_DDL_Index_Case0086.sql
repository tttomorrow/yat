--  @testpoint: expression：一般操作符
DROP TABLE if EXISTS test_index_table_086 CASCADE;
create table test_index_table_086(
c_float1 float
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_086 values(i);
    end loop;
end;
/

--建btree索引:5-5
drop index if exists index_086_01;
create index index_086_01 on test_index_table_086 using btree(c_float1+1) ;
select relname from pg_class where relname like 'index_086_%' order by relname;


--建btree索引:5%4
drop index if exists index_086_01;
create index index_086_01 on test_index_table_086 using btree(c_float1%4) ;
select relname from pg_class where relname like 'index_086_%' order by relname;


--建btree索引:91&15
drop index if exists index_086_01;
create index index_086_01 on test_index_table_086 using btree(c_float1&15);
select relname from pg_class where relname like 'index_086_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_086 CASCADE;
