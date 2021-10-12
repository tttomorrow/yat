-- @testpoint:  create index:table_name：列存普通表的index：success
--删表
drop table if exists test_index_table_015 cascade;
create table test_index_table_015(id int) WITH (ORIENTATION = column);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_015 values(i);
  end LOOP;
end;
/

--建同义词
explain select * from test_index_table_015 where id = 6541;
--创建索引
drop index if exists index_015;
create index index_015 on test_index_table_015(id);
explain select * from test_index_table_015 where id = 6541;
select relname from pg_class where relname='index_015';
--清理数据
drop index if exists index_015;
drop table if exists test_index_table_015 cascade;