-- @testpoint: opengauss关键字final(非保留)，自定义数据类型名为final 合理报错
--关键字final作为数据类型不带引号，创建成功
drop type if exists public.final;
CREATE TYPE public.final AS (f1 int, f2 text);
select typname from pg_type where typname ='public.final';
drop type public.final;

--关键字final作为数据类型加双引号，创建成功
drop type if exists "public.final";
CREATE TYPE "public.final" AS (f1 int, f2 text);
select typname from pg_type where typname ='public.final';
drop type "public.final";

--关键字final作为数据类型加单引号，合理报错
drop type if exists 'public.final';
CREATE TYPE 'public.final' AS (f1 int, f2 text);


--关键字final作为数据类型加反引号，合理报错
drop type if exists `public.final`;
CREATE TYPE `public.final` AS (f1 int, f2 text);
