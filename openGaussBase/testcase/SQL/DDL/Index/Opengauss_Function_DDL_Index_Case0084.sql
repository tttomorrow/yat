--  @testpoint: expression：与已有函数结合使用

DROP TABLE if EXISTS test_index_table_084 CASCADE;
create table test_index_table_084(
c_float1 float
) WITH (ORIENTATION = row) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_084 values(i);
    end loop;
end;
/

--建btree索引:包含char_length函数
drop index if exists index_084_01;
create index index_084_01 on test_index_table_084 using btree(char_length(c_float1));
select relname from pg_class where relname like 'index_084_%' order by relname;

--建btree索引：包含mod函数
drop index if exists index_084_01;
create index index_084_01 on test_index_table_084 using btree(mod(c_float1,1));
select relname from pg_class where relname like 'index_084_%' order by relname;

--建btree索引：包含cast函数
drop index if exists index_084_01;
create index index_084_01 on test_index_table_084 using btree(cast(c_float1 as int));
select relname from pg_class where relname like 'index_084_%' order by relname;


--清理环境
DROP TABLE if EXISTS test_index_table_084 CASCADE;
