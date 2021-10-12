--  @testpoint:opengauss关键字distribute(非保留)，自定义数据类型名为distribute
--关键字distribute作为数据类型不带引号，创建成功
drop type if exists distribute;
CREATE TYPE distribute AS (f1 int, f2 text);
select typname from pg_type where typname ='distribute';
drop type distribute;


--关键字distribute作为用户名加双引号，创建成功
drop type if exists "distribute";
CREATE TYPE "distribute" AS (f1 int, f2 text);
select typname from pg_type where typname ='distribute';
drop type "distribute";

--关键字distribute作为用户名加单引号，合理报错
drop type if exists 'distribute';
CREATE TYPE 'distribute' AS (f1 int, f2 text);
select * from pg_type where typname ='distribute';
drop type 'distribute';

--关键字distribute作为用户名加反引号，合理报错
drop type if exists `distribute`;
CREATE TYPE `distribute` AS (f1 int, f2 text);
select * from pg_type where typname =`distribute`;
drop type `distribute`;