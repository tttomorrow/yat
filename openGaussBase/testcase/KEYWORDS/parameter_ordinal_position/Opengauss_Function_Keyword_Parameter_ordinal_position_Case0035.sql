--  @testpoint:opengauss关键字parameter_ordinal_position(非保留)，自定义数据类型名为explain
--关键字explain作为数据类型不带引号，创建成功
drop type if exists parameter_ordinal_position;
CREATE TYPE parameter_ordinal_position AS (f1 int, f2 text);
select typname from pg_type where typname ='parameter_ordinal_position';
drop type parameter_ordinal_position;


--关键字explain作为数据类型加双引号，创建成功
drop type if exists "parameter_ordinal_position";
CREATE TYPE "parameter_ordinal_position" AS (f1 int, f2 text);
select typname from pg_type where typname ='parameter_ordinal_position';
drop type "parameter_ordinal_position";

--关键字explain作为数据类型加单引号，合理报错
drop type if exists 'parameter_ordinal_position';
CREATE TYPE 'parameter_ordinal_position' AS (f1 int, f2 text);
select * from pg_type where typname ='parameter_ordinal_position';
drop type 'parameter_ordinal_position';

--关键字explain作为数据类型加反引号，合理报错
drop type if exists `parameter_ordinal_position`;
CREATE TYPE `parameter_ordinal_position` AS (f1 int, f2 text);
select * from pg_type where typname =`parameter_ordinal_position`;
drop type `parameter_ordinal_position`;