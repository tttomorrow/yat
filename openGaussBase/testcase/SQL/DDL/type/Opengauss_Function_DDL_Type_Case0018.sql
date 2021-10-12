--  @testpoint:给复合类型增加新的属性
--创建复合类型
drop type if exists test2_type cascade;
create type test2_type as(a int,b text);
--增加属性
ALTER TYPE test2_type ADD ATTRIBUTE c numeric;
--建表
drop table if exists test_t1 cascade;
create table test_t1 (id int,d test2_type);
--插入数据
insert into test_t1 values(1,(1,'lisi',1.99));
--查询
select * from test_t1;
--删除类型
drop type if exists test2_type cascade;
--删除表
drop table if exists test_t1 cascade;