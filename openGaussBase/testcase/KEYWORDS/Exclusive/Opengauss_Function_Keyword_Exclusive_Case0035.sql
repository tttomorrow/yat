-- @testpoint: opengauss关键字exclusive(非保留)，自定义数据类型名为exclusive 合理报错
--关键字exclusive作为数据类型不带引号，创建成功
drop type if exists public.exclusive;
CREATE TYPE public.exclusive AS (f1 int, f2 text);
select typname from pg_type where typname ='public.exclusive';
drop type public.exclusive;

--关键字exclusive作为数据类型加双引号，创建成功
drop type if exists "public.exclusive";
CREATE TYPE "public.exclusive" AS (f1 int, f2 text);
select typname from pg_type where typname ='public.exclusive';
drop type "public.exclusive";

--关键字exclusive作为数据类型加单引号，合理报错
drop type if exists 'public.exclusive';
CREATE TYPE 'public.exclusive' AS (f1 int, f2 text);
select * from pg_type where typname ='public.exclusive';
drop type 'public.exclusive';

--关键字exclusive作为数据类型加反引号，合理报错
drop type if exists `public.exclusive`;
CREATE TYPE `public.exclusive` AS (f1 int, f2 text);
select * from pg_type where typname =`public.exclusive`;
drop type `public.exclusive`;