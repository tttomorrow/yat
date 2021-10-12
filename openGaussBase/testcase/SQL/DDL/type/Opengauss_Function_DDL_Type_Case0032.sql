--  @testpoint:为枚举类型增加一个新值，new_enum_value为空，合理报错
--创建枚举类型
drop type if exists bugstatus2 cascade;
CREATE TYPE bugstatus2 AS ENUM ('create', 'modify', 'closed');
--为枚举类型增加一个新值，合理报错
ALTER TYPE bugstatus2 ADD VALUE '' BEFORE 'create';
--删除类型
drop type bugstatus2 cascade;