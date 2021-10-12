-- @testpoint: opengauss关键字fetch(保留)，自定义数据类型名为fetch 合理报错
--关键字fetch作为数据类型不带引号，创建成功
drop type if exists public.fetch;
CREATE TYPE public.fetch AS (f1 int, f2 text);
drop type if exists public.fetch;
--关键字fetch作为数据类型加双引号，创建成功
drop type if exists public."fetch";
CREATE TYPE public."fetch" AS (f1 int, f2 text);
select typname from pg_type where typname = 'fetch';
drop type if exists public."fetch";

--关键字fetch作为数据类型加单引号，合理报错
drop type if exists 'public.fetch';
CREATE TYPE 'public.fetch' AS (f1 int, f2 text);


--关键字fetch作为数据类型加反引号，合理报错
drop type if exists `public.fetch`;
CREATE TYPE `public.fetch` AS (f1 int, f2 text);
