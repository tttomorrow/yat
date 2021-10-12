-- @testpoint: opengauss关键字extract(非保留)，自定义数据类型名为extract，作为数据类型加单引号或反引号时合理报错

--关键字extract作为数据类型不带引号，创建成功
drop type if exists public.extract;
create type extract as (f1 int, f2 text);
select typname from pg_type where typname ='extract';
drop type public.extract;

--关键字extract作为数据类型加双引号，创建成功
drop type if exists "public.extract";
create type "extract" as (f1 int, f2 text);
select typname from pg_type where typname ='extract';
drop type public."extract";

--关键字extract作为数据类型加单引号，合理报错
drop type if exists 'public.extract';
create type 'extract' as (f1 int, f2 text);

--关键字extract作为数据类型加反引号，合理报错
drop type if exists public.`extract`;
create type `extract` as (f1 int, f2 text);
