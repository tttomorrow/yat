-- @testpoint: opengauss关键字exec(非保留)，自定义数据类型名为exec 合理报错
--关键字exec作为数据类型不带引号，创建成功
drop type if exists public.exec;
CREATE TYPE public.exec AS (f1 int, f2 text);
select typname from pg_type where typname ='public.exec';
drop type public.exec;

--关键字exec作为数据类型加双引号，创建成功
drop type if exists "public.exec";
CREATE TYPE "public.exec" AS (f1 int, f2 text);
select typname from pg_type where typname ='public.exec';
drop type "public.exec";

--关键字exec作为数据类型加单引号，合理报错
drop type if exists 'public.exec';
CREATE TYPE 'public.exec' AS (f1 int, f2 text);
select * from pg_type where typname ='public.exec';
drop type 'public.exec';

--关键字exec作为数据类型加反引号，合理报错
drop type if exists `public.exec`;
CREATE TYPE `public.exec` AS (f1 int, f2 text);
select * from pg_type where typname =`public.exec`;
drop type `public.exec`;