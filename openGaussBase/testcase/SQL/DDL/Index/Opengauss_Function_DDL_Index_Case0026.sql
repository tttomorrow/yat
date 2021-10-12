-- @testpoint: USING method：行存组合索引：单表多字段:success
--删表
drop table if exists test_index_table_026 cascade;
create table test_index_table_026(id int, name varchar) ;
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_026 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--创建索引
drop index if exists index_026;
create index index_026 on test_index_table_026 using btree(id,name);
explain select * from test_index_table_026 where id=15 or name='zhangsan20';
select relname from pg_class where relname='index_026';

--清理数据
drop index if exists index_026;
drop table if exists test_index_table_026 cascade;