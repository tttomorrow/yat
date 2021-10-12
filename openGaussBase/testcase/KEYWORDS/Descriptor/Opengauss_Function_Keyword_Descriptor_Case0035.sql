--  @testpoint:opengauss关键字descriptor(非保留)，自定义数据类型名为descriptor
--关键字descriptor作为数据类型不带引号，创建成功
drop type if exists descriptor;
CREATE TYPE descriptor AS (f1 int, f2 text);
select typname from pg_type where typname ='descriptor';
drop type descriptor;


--关键字descriptor作为数据类型加双引号，创建成功
drop type if exists "descriptor";
CREATE TYPE "descriptor" AS (f1 int, f2 text);
select typname from pg_type where typname ='descriptor';
drop type "descriptor";

--关键字descriptor作为数据类型加单引号，合理报错
drop type if exists 'descriptor';
CREATE TYPE 'descriptor' AS (f1 int, f2 text);


--关键字descriptor作为数据类型加反引号，合理报错
drop type if exists `descriptor`;
CREATE TYPE `descriptor` AS (f1 int, f2 text);
