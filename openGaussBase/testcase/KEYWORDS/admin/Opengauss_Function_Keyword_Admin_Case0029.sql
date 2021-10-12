--  @testpoint:opengauss关键字admin(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists admin;
CREATE TABLESPACE admin RELATIVE LOCATION 'tablespace/tablespace_1';
--清理环境
drop tablespace admin;

--关键字带双引号，创建成功
drop tablespace if exists "admin";
CREATE TABLESPACE "admin" RELATIVE LOCATION 'tablespace/tablespace_1'; 

--清理环境
drop tablespace "admin";

--关键字带单引号，合理报错
drop tablespace if exists 'admin';

--关键字带反引号，合理报错
drop tablespace if exists `admin`;
