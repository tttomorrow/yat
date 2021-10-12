--  @testpoint:opengauss关键字access(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists access;
CREATE TABLESPACE access RELATIVE LOCATION 'tablespace/tablespace_1';
--清理环境
drop tablespace access;

--关键字带双引号，创建成功
drop tablespace if exists "access";
CREATE TABLESPACE "access" RELATIVE LOCATION 'tablespace/tablespace_1'; 

--清理环境
drop tablespace "access";

--关键字带单引号，合理报错
drop tablespace if exists 'access';

--关键字带反引号，合理报错
drop tablespace if exists `access`;
