-- @testpoint: 事务块内部不可以创建tablespace，合理报错

--step1: 事务块内创建表空间;expect: 创建失败
drop tablespace if exists tsp_tbspc0013;
begin;/
create tablespace tsp_tbspc0013 relative location 'tbspc0013_location';
end;
--step2: 非事务块内创建表空间;expect: 创建成功
create tablespace tsp_tbspc0013 relative location 'tbspc0013_location';
--step3: 清理表空间;expect: 清理成功
drop tablespace if exists tsp_tbspc0013;