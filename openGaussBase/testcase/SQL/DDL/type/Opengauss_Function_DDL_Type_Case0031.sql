--  @testpoint:为枚举类型增加一个新值，neighbor_enum_value不存在，合理报错
--创建枚举类型
drop type if exists bugstatus1 cascade;
CREATE TYPE bugstatus1 AS ENUM ('create', 'modify', 'closed');
--为枚举类型增加一个新值
ALTER TYPE bugstatus1 ADD VALUE 'insert' BEFORE 'create1';
ALTER TYPE bugstatus1 ADD VALUE 'delete' after 'create1';
--删除类型
drop type if exists bugstatus1 cascade;