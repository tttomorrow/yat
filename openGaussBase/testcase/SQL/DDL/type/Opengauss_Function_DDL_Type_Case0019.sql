--  @testpoint:改变类型名称
--创建类型
drop type if exists test2_type cascade;
create type test2_type as(a int,b text);
--改变类型的名称
ALTER TYPE test2_type RENAME TO new_test2_type;
--查询类型
select typname,typtype from pg_type where typname = 'new_test2_type';
--删除类型
drop type if exists new_test2_type cascade;