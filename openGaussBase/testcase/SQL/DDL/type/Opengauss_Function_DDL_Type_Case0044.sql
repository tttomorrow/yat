--  @testpoint:复合类型中，在一条命令中增加一个属性并且删除一个属性
--创建类型
drop type if exists t_compfoo cascade;
CREATE TYPE t_compfoo AS (f1 int, f2 text);
--增加一个属性并且删除一个属性
ALTER TYPE t_compfoo ADD ATTRIBUTE f3 numeric, drop ATTRIBUTE f1;
--建表
drop table if exists test_1 cascade;
create table test_1(a t_compfoo);
--插入数据
insert into test_1 values(('meat',1.578));
--查询
 select * from test_1;
--删除表
drop table test_1 cascade;