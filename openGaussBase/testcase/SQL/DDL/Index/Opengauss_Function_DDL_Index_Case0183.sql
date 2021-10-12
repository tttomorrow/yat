-- @testpoint:  先建索引再insert3W数据

--建普通表
DROP TABLE if EXISTS test_index_table_183 CASCADE;
create table test_index_table_183(c_char2000 char(2000),c_varchar1900 varchar(1900) );

drop index if exists index_183_01;
create index index_183_01 on test_index_table_183(c_char2000,c_varchar1900);
select relname from pg_class where relname like 'index_183_%';


begin
    for i in 0..30000 loop
        insert into test_index_table_183 values(i,i);
    end loop;
end;
/

explain select * from test_index_table_183 where c_char2000 = '50' group by c_char2000,c_varchar1900;

--清理环境
DROP TABLE if EXISTS test_index_table_183 CASCADE;
