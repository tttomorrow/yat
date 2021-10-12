-- @testpoint: opengauss关键字false(保留)，自定义数据类型名为false，作为数据类型加单引号或反引号时合理报错
--关键字false作为数据类型不带引号，合理报错
drop type if exists public.false;
CREATE TYPE false AS (f1 int, f2 text);

--关键字false作为数据类型加双引号，创建成功
drop type if exists public."false";
CREATE TYPE "false" AS (f1 int, f2 text);
select typname from pg_type where typname ='false';
drop type public."false";

--关键字false作为数据类型加单引号，合理报错
drop type if exists public.'false';
CREATE TYPE 'false' AS (f1 int, f2 text);


--关键字false作为数据类型加反引号，合理报错
drop type if exists public.`false`;
CREATE TYPE `false` AS (f1 int, f2 text);
