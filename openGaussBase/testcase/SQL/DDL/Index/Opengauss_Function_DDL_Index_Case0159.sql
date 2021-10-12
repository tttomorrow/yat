--  @testpoint:增加列和删除列建索引

--建普通表
DROP TABLE if EXISTS test_index_table_159 CASCADE;
create table test_index_table_159(
c_point point);

--建索引
drop index if exists index_159_01;
create index index_159_01 on test_index_table_159 using gist(c_point);
select relname from pg_class where relname like 'index_159_%' order by relname;

--插入数据
begin
    for i in 0..10000 loop
        insert into test_index_table_159 values(point(i,i));
    end loop;
end;
/

--truncate
explain select * from test_index_table_159 where c_point <^ point(50,50);
truncate test_index_table_159;
explain select * from test_index_table_159 where c_point <^ point(50,50);

--reindex
alter index index_159_01 UNUSABLE;
explain select * from test_index_table_159 where c_point <^ point(50,50);
REINDEX INDEX  index_159_01;
explain select * from test_index_table_159 where c_point <^ point(50,50);

alter table test_index_table_159 add column c_int int;
explain select c_int from test_index_table_159 where c_int > 500 group by c_int;
--建索引
drop index if exists index_159_02;
create index index_159_02 on test_index_table_159 using btree(c_int);
select relname from pg_class where relname like 'index_159_%' order by relname;
explain select c_int from test_index_table_159 where c_int > 500 group by c_int;

--插入数据
begin
    for i in 0..10000 loop
        insert into test_index_table_159(c_int) values(i);
    end loop;
end;
/

explain select c_int from test_index_table_159 where c_int > 500 group by c_int;

alter table test_index_table_159 drop column c_point;
select relname from pg_class where relname like 'index_159_%' order by relname;
explain select * from test_index_table_159 where c_point <^ point(50,50);

--清理环境
DROP TABLE if EXISTS test_index_table_159 CASCADE;
