--  @testpoint: USING method：行存组合索引：跨表建立索引：合理报错
--删表
drop table if exists test_index_table1_027 cascade;
drop table if exists test_index_table2_027 cascade;
create table test_index_table1_027(id int, name varchar) ;
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table1_027 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
drop table if exists test_index_table2_027 cascade;
create table test_index_table2_027(id int, name varchar) ;
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table2_027 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--创建索引
drop index if exists index_027;
create index index_027 on test_index_table1_027(id) and test_index_table2_027(name);
explain select * from test_index_table1_027 t1 join test_index_table2_027 t2 on t1.id=t2.id where id=15 or name='zhangsan20';
select relname from pg_class where relname='index_027';

--清理数据
drop index if exists index_027;
drop table if exists test_index_table1_027 cascade;
drop table if exists test_index_table2_027 cascade;