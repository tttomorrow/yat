--  @testpoint:opengauss关键字path(非保留)，自定义数据类型名为path
--关键字path作为数据类型不带引号，创建成功
drop type if exists public.path;
CREATE TYPE path AS (f1 int, f2 text);
select typname from pg_type where typname ='path';
drop type public.path;


--关键字path作为数据类型加双引号，创建成功
drop type if exists public."path";
CREATE TYPE "path" AS (f1 int, f2 text);
select typname from pg_type where typname ='path';
drop type public."path";

--关键字path作为数据类型加单引号，合理报错
drop type if exists public.'path';
CREATE TYPE 'path' AS (f1 int, f2 text);
select * from pg_type where typname ='path';
drop type public.'path';

--关键字path作为数据类型加反引号，合理报错
drop type if exists `path`;
CREATE TYPE `path` AS (f1 int, f2 text);
select * from pg_type where typname =`path`;
drop type public.`path`;
