--  @testpoint:opengauss关键字coalesce(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists coalesce;
CREATE TABLESPACE coalesce RELATIVE LOCATION 'tablespace/tablespace_1';
--清理环境
drop tablespace coalesce;

--关键字带双引号，创建成功
drop tablespace if exists "coalesce";
CREATE TABLESPACE "coalesce" RELATIVE LOCATION 'tablespace/tablespace_1'; 

--清理环境
drop tablespace "coalesce";

--关键字带单引号，合理报错
drop tablespace if exists 'coalesce';

--关键字带反引号，合理报错
drop tablespace if exists `coalesce`;
