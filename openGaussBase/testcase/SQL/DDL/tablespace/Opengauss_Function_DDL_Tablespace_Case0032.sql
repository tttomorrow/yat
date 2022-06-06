-- @testpoint: 事务块内部不可以删除tablespace，合理报错

--step1: 创建表空间;expect: 创建成功
drop tablespace if exists tsp_tbspc0032;
create tablespace tsp_tbspc0032 relative location 'tbspc0032_location';
--step2: 事务块内删除表空间;expect: 删除失败
begin;/
drop tablespace tsp_tbspc0032;
end;
--step3: 非事务块内删除表空间;expect: 删除成功
drop tablespace tsp_tbspc0032;