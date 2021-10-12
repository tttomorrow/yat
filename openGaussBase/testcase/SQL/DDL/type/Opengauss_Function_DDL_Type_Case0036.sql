--  @testpoint:重命名枚举类型的一个标签值
--创建枚举类型
drop type if exists bugstatus3 cascade;
CREATE TYPE bugstatus3 AS ENUM ('create', 'modify', 'closed');
--重命名枚举类型的一个标签值,枚举值不存在，合理报错
ALTER TYPE bugstatus3 RENAME VALUE 'create1' TO 'delete';
--删除类型
drop type bugstatus3 cascade;