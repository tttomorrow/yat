--  @testpoint:opengauss关键字plans(非保留)，自定义数据类型名为plans
--关键字plans作为数据类型不带引号，创建成功
drop type if exists plans;
CREATE TYPE plans AS (f1 int, f2 text);
select typname from pg_type where typname ='plans';
drop type plans;


--关键字plans作为数据类型加双引号，创建成功
drop type if exists "plans";
CREATE TYPE "plans" AS (f1 int, f2 text);
select typname from pg_type where typname ='plans';
drop type "plans";

--关键字plans作为数据类型加单引号，合理报错
drop type if exists 'plans';
CREATE TYPE 'plans' AS (f1 int, f2 text);
select * from pg_type where typname ='plans';
drop type 'plans';

--关键字plans作为数据类型加反引号，合理报错
drop type if exists `plans`;
CREATE TYPE `plans` AS (f1 int, f2 text);
select * from pg_type where typname =`plans`;
drop type `plans`;