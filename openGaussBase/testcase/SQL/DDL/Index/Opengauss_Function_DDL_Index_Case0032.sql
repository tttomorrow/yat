-- @testpoint: USING method：行存local临时表btree组合索引：success
--建表
drop table if exists test_index_table_032;
create TEMPORARY table test_index_table_032(id int, name varchar) with (orientation=row);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_032 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--创建索引
drop index if exists index_032;
create index index_032 on test_index_table_032 using btree(id,name);
explain select * from test_index_table_032 where id=15 or name='zhangsan20';
select relname from pg_class where relname='index_032';
--清理数据
drop index if exists index_032;
DROP TABLE if EXISTS test_index_table_032 CASCADE;