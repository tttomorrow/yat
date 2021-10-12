--  @testpoint:opengauss关键字parameters(非保留)，自定义数据类型名为parameters
--关键字parameters作为数据类型不带引号，创建成功
drop type if exists parameters;
CREATE TYPE parameters AS (f1 int, f2 text);
select typname from pg_type where typname ='parameters';
drop type parameters;


--关键字parameters作为数据类型加双引号，创建成功
drop type if exists "parameters";
CREATE TYPE "parameters" AS (f1 int, f2 text);
select typname from pg_type where typname ='parameters';
drop type "parameters";

--关键字parameters作为数据类型加单引号，合理报错
drop type if exists 'parameters';
CREATE TYPE 'parameters' AS (f1 int, f2 text);
select typname from pg_type where typname ='parameters';
drop type 'parameters';

--关键字parameters作为数据类型加反引号，合理报错
drop type if exists `parameters`;
CREATE TYPE `parameters` AS (f1 int, f2 text);
select typname from pg_type where typname =`parameters`;
drop type `parameters`;
