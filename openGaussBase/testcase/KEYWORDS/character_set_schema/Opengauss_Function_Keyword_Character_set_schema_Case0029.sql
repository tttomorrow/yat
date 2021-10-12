--  @testpoint:opengauss关键字character_set_schema(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists character_set_schema;
CREATE TABLESPACE character_set_schema RELATIVE LOCATION 'tablespace/tablespace_1';
--清理环境
drop tablespace character_set_schema;

--关键字带双引号，创建成功
drop tablespace if exists "character_set_schema";
CREATE TABLESPACE "character_set_schema" RELATIVE LOCATION 'tablespace/tablespace_1'; 

--清理环境
drop tablespace "character_set_schema";

--关键字带单引号，合理报错
drop tablespace if exists 'character_set_schema';

--关键字带反引号，合理报错
drop tablespace if exists `character_set_schema`;
