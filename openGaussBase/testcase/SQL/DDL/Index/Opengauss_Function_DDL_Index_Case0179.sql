-- @testpoint:  char长度：3900+3901

--建普通表
DROP TABLE if EXISTS test_index_table_179 CASCADE;
create table test_index_table_179(c_char3900 char(3900),c_char3901 char(3901) );

begin
    for i in 0..1000 loop
        insert into test_index_table_179 values(i,i);
    end loop;
end;
/

drop index if exists index_179_01;
drop index if exists index_179_02;
create index index_179_01 on test_index_table_179(c_char3900);
create index index_179_02 on test_index_table_179(c_char3901);
select relname from pg_class where relname like 'index_179_%';
explain select c_char3900 from test_index_table_179 where c_char3900 = '50' group by c_char3900;
explain select c_char3901 from test_index_table_179 where c_char3901 = '50' group by c_char3901;

--清理环境
DROP TABLE if EXISTS test_index_table_179 CASCADE;