--  @testpoint:opengauss关键字delete(非保留)，自定义数据类型名为delete
--关键字delete作为数据类型不带引号，创建成功
drop type if exists delete;
CREATE TYPE delete AS (f1 int, f2 text);
select typname from pg_type where typname ='delete';
drop type delete;


--关键字delete作为用户名加双引号，创建成功
drop type if exists "delete";
CREATE TYPE "delete" AS (f1 int, f2 text);
select typname from pg_type where typname ='delete';
drop type "delete";

--关键字delete作为用户名加单引号，合理报错
drop type if exists 'delete';
CREATE TYPE 'delete' AS (f1 int, f2 text);
select typname from pg_type where typname ='delete';
drop type 'delete';

--关键字delete作为用户名加反引号，合理报错
drop type if exists `delete`;
CREATE TYPE `delete` AS (f1 int, f2 text);
select typname from pg_type where typname =`delete`;
drop type `delete`;
