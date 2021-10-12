--  @testpoint:改变一个复合类型中的一个属性的名称
--创建类型
drop type if exists test2_type cascade;
create type test2_type as(a int,b text);
--修改属性名称
ALTER TYPE test2_type RENAME ATTRIBUTE a to new_a;
--删除类型
drop type test2_type cascade;
