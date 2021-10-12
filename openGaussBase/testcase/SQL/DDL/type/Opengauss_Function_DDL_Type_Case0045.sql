--  @testpoint:创建类型在列存表使用类型，合理报错
--创建类型
drop type if exists t_compfoo cascade;
CREATE TYPE t_compfoo AS (f1 int, f2 text);
--建表,其中一列字段定义类型为t_compfoo，合理报错
drop table if exists test_1 cascade;
create table test_1(a t_compfoo)with(orientation = column);
--删除类型
drop type t_compfoo cascade;