--  @testpoint: 修改索引字段类型和长度查看索引

--建普通表
DROP TABLE if EXISTS test_index_table_187 CASCADE;
create table test_index_table_187(
c_int int);

drop index if exists index_187_01;
create index index_187_01 on test_index_table_187(c_int) ;
select relname from pg_class where relname like 'index_187_%';
explain select * from test_index_table_187 where c_int >= 50 group by c_int;

--修改索引列类型
alter table test_index_table_187 modify c_int varchar;
explain select * from test_index_table_187 where c_int >= 50 group by c_int;
explain select * from test_index_table_187 where c_int = '50' group by c_int;
alter table test_index_table_187 modify c_int varchar(3900);
explain select * from test_index_table_187 where c_int = '3000' group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_187 CASCADE;