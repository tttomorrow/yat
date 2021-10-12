--  @testpoint:创建枚举类型,标签名为空字符串，合理报错
--标签名为空，合理报错
drop type if exists bugstatus;
CREATE TYPE bugstatus AS ENUM ('');
--标签名为null，合理报错
drop type if exists bugstatus1;
CREATE TYPE bugstatus1 AS ENUM (null);