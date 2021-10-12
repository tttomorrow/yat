--  @testpoint:一般表达式索引

--建普通表
DROP TABLE if EXISTS test_index_table_189 CASCADE;
create table test_index_table_189(
c_varchar varchar(3900));

begin
    for i in 0..10000 loop
        insert into test_index_table_189 values(to_char(lpad('test',3900,'x')));
    end loop;
end;
/

select count(8) from test_index_table_189;
drop index if exists index_189_01;
create index index_189_01 on test_index_table_189(c_varchar || c_varchar);
select relname from pg_class where relname like 'index_189_%';
explain select * from test_index_table_189 where c_varchar || c_varchar = 'te st' group by c_varchar;

--清理环境
DROP TABLE if EXISTS test_index_table_189 CASCADE;