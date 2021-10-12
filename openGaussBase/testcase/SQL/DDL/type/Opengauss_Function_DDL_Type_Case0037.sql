--  @testpoint:从复合类型删除一个属性，IF EXISTS选项测试
--创建类型
drop type if exists test4_type cascade;
create type test4_type as(a int,b text);
--删除属性a,添加IF EXISTS，删除成功
ALTER TYPE test4_type DROP ATTRIBUTE IF EXISTS a;
--删除不存在的属性，发出notice
ALTER TYPE test4_type DROP ATTRIBUTE IF EXISTS c;
--删除类型
drop type test4_type cascade;