-- @testpoint: USING method：列存local临时表psort组合索引：success
--建表
drop table if exists test_index_table_036;
create TEMPORARY table test_index_table_036(id int, name varchar) with (orientation=column);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_036 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--创建索引
drop index if exists index_036;
create index index_036 on test_index_table_036 using psort(id,name);
explain select * from test_index_table_036 where id=15 or name='zhangsan20';
select relname from pg_class where relname='index_036';

drop index if exists index_036;
DROP TABLE if EXISTS test_index_table_036 CASCADE;