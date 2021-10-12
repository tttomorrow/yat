-- @testpoint: USING method：列存组合psort索引：单表多字段29:success
--删表
drop table if exists test_index_table_029 cascade;
create table test_index_table_029(id int, name varchar) with (orientation=column);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_029 values(i,concat('zhangsan',i));
  end LOOP;
end;
/
--创建索引
drop index if exists index_029;
create index index_029 on test_index_table_029 using psort(id,name);
explain select * from test_index_table_029 where id=15 or name='zhangsan20';
select relname from pg_class where relname='index_029';

--清理数据
drop index if exists index_029;
drop table if exists test_index_table_029 cascade;