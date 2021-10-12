--  @testpoint:opengauss关键字before(非保留)，为枚举类型增加一个新值
--创建枚举类型
CREATE TYPE bugstatus AS ENUM ('create', 'modify', 'closed');
--查询枚举类型
select enumlabel from pg_enum;
--为枚举类型增加一个新值
ALTER TYPE bugstatus ADD VALUE IF NOT EXISTS  'hello' AFTER  'closed';
--查询枚举类型
select enumlabel from pg_enum;
--清理环境
drop type bugstatus;


