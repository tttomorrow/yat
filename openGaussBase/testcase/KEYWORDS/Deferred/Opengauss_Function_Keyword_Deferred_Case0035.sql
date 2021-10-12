--  @testpoint:opengauss关键字deferred(非保留)，自定义数据类型名为deferred
--关键字deferred作为数据类型不带引号，创建成功
drop type if exists deferred;
CREATE TYPE deferred AS (f1 int, f2 text);
select typname from pg_type where typname ='deferred';
drop type deferred;


--关键字deferred作为数据类型加双引号，创建成功
drop type if exists "deferred";
CREATE TYPE "deferred" AS (f1 int, f2 text);
select typname from pg_type where typname ='deferred';
drop type "deferred";

--关键字deferred作为数据类型加单引号，合理报错
drop type if exists 'deferred';
CREATE TYPE 'deferred' AS (f1 int, f2 text);


--关键字deferred作为数据类型加反引号，合理报错
drop type if exists `deferred`;
CREATE TYPE `deferred` AS (f1 int, f2 text);
