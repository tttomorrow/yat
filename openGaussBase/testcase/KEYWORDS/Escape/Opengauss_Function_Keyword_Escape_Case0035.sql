--  @testpoint:opengauss关键字escape(非保留)，自定义数据类型名为escape
--关键字escape作为数据类型不带引号，创建成功
drop type if exists escape;
CREATE TYPE escape AS (f1 int, f2 text);
select typname from pg_type where typname ='escape';
drop type escape;


--关键字escape作为数据类型加双引号，创建成功
drop type if exists "escape";
CREATE TYPE "escape" AS (f1 int, f2 text);
select typname from pg_type where typname ='escape';
drop type "escape";

--关键字escape作为数据类型加单引号，合理报错
drop type if exists 'escape';
CREATE TYPE 'escape' AS (f1 int, f2 text);
select * from pg_type where typname ='escape';
drop type 'escape';

--关键字escape作为数据类型加反引号，合理报错
drop type if exists `escape`;
CREATE TYPE `escape` AS (f1 int, f2 text);
select * from pg_type where typname =`escape`;
drop type `escape`;