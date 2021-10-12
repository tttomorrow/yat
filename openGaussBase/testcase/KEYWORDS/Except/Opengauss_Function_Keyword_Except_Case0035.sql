-- @testpoint: opengauss关键字except(保留)，自定义数据类型名为except 合理报错

--关键字except作为数据类型不带引号，创建成功

drop type if exists public.except;
CREATE TYPE public.except AS (f1 int, f2 text);
drop type if exists public.except;
--关键字except作为数据类型加双引号，创建成功
drop type if exists public."except";
CREATE TYPE public."except" AS (f1 int, f2 text);
select typname from pg_type where typname ='except';
drop type public."except";

--关键字except作为数据类型加单引号，合理报错
drop type if exists 'public.except';
CREATE TYPE 'public.except' AS (f1 int, f2 text);


--关键字except作为数据类型加反引号，合理报错
drop type if exists `public.except`;
CREATE TYPE `public.except` AS (f1 int, f2 text);
