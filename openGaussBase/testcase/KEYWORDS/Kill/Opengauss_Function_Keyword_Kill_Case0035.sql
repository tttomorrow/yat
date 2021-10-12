--  @testpoint:opengauss关键字Kill(非保留)，自定义数据类型名为explain
--关键字explain作为数据类型不带引号，创建成功
drop type if exists Kill;
CREATE TYPE Kill AS (f1 int, f2 text);
select typname from pg_type where typname ='Kill';
drop type Kill;


--关键字explain作为数据类型加双引号，创建成功
drop type if exists "Kill";
CREATE TYPE "Kill" AS (f1 int, f2 text);
select typname from pg_type where typname ='Kill';
drop type "Kill";

--关键字explain作为数据类型加单引号，合理报错
drop type if exists 'Kill';
CREATE TYPE 'Kill' AS (f1 int, f2 text);
select * from pg_type where typname ='Kill';
drop type 'Kill';

--关键字explain作为数据类型加反引号，合理报错
drop type if exists `Kill`;
CREATE TYPE `Kill` AS (f1 int, f2 text);
select * from pg_type where typname =`Kill`;
drop type `Kill`;