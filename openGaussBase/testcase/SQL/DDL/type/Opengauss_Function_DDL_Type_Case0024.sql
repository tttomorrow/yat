--  @testpoint:复合类型删除一个属性
--创建类型
drop type if exists test2_type cascade;
create type test2_type as(a int,b text);
--删除属性
ALTER TYPE test2_type DROP ATTRIBUTE a;
--删除不存在的属性，添加if exists,不会抛出错误
ALTER TYPE test2_type DROP ATTRIBUTE if exists a;
--删除不存在的属性，省略if exists,合理报错
ALTER TYPE test2_type DROP ATTRIBUTE a;
--删除类型
drop type if exists test2_type cascade;