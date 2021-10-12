--  @testpoint:varchar长度：3900+3901

--建普通表
DROP TABLE if EXISTS test_index_table_180 CASCADE;
create table test_index_table_180(c_varchar3900 varchar(3900),c_varchar3901 varchar(3901) );

begin
    for i in 0..1000 loop
        insert into test_index_table_180 values(i,i);
    end loop;
end;
/

drop index if exists index_180_01;
drop index if exists index_180_02;
create index index_180_01 on test_index_table_180(c_varchar3900);
create index index_180_02 on test_index_table_180(c_varchar3901);
select relname from pg_class where relname like 'index_180_%';
explain select c_varchar3900 from test_index_table_180 where c_varchar3900 = '50' group by c_varchar3900;
explain select c_varchar3901 from test_index_table_180 where c_varchar3901 = '50' group by c_varchar3901;

--清理环境
DROP TABLE if EXISTS test_index_table_180 CASCADE;