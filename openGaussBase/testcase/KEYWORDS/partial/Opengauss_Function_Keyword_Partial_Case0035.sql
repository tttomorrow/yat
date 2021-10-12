--  @testpoint:opengauss关键字partial(非保留)，自定义数据类型名为partial
--关键字partial作为数据类型不带引号，创建成功
drop type if exists partial;
CREATE TYPE partial AS (f1 int, f2 text);
select typname from pg_type where typname ='partial';
drop type partial;


--关键字partial作为数据类型加双引号，创建成功
drop type if exists "partial";
CREATE TYPE "partial" AS (f1 int, f2 text);
select typname from pg_type where typname ='partial';
drop type "partial";

--关键字partial作为数据类型加单引号，合理报错
drop type if exists 'partial';
CREATE TYPE 'partial' AS (f1 int, f2 text);
select * from pg_type where typname ='partial';
drop type 'partial';

--关键字partial作为数据类型加反引号，合理报错
drop type if exists `partial`;
CREATE TYPE `partial` AS (f1 int, f2 text);
select * from pg_type where typname =`partial`;
drop type `partial`;