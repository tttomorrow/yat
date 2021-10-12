-- @testpoint: USING method：行存local临时表psort组合索引：合理报错
--建表
drop table if exists test_index_table_033;
create TEMPORARY table test_index_table_033(id int, name varchar) with (orientation=row);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_033 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--创建索引
drop index if exists index_033;
create index index_033 on test_index_table_033 using psort(id,name);
explain select * from test_index_table_033 where id=15 or name='zhangsan20';
select relname from pg_class where relname='index_033';

drop index if exists index_033;
DROP TABLE if EXISTS test_index_table_033 CASCADE;