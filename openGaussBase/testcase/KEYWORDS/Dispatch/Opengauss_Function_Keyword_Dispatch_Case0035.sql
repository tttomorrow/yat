--  @testpoint:opengauss关键字dispatch(非保留)，自定义数据类型名为dispatch
--关键字dispatch作为数据类型不带引号，创建成功
drop type if exists dispatch;
CREATE TYPE dispatch AS (f1 int, f2 text);
select typname from pg_type where typname ='dispatch';
drop type dispatch;


--关键字dispatch作为用户名加双引号，创建成功
drop type if exists "dispatch";
CREATE TYPE "dispatch" AS (f1 int, f2 text);
select typname from pg_type where typname ='dispatch';
drop type "dispatch";

--关键字dispatch作为用户名加单引号，合理报错
drop type if exists 'dispatch';
CREATE TYPE 'dispatch' AS (f1 int, f2 text);
select * from pg_type where typname ='dispatch';
drop type 'dispatch';

--关键字dispatch作为用户名加反引号，合理报错
drop type if exists `dispatch`;
CREATE TYPE `dispatch` AS (f1 int, f2 text);
select * from pg_type where typname =`dispatch`;
drop type `dispatch`;