--  @testpoint:opengauss关键字enable(非保留)，自定义数据类型名为enable
--关键字enable作为数据类型不带引号，创建成功
drop type if exists enable;
CREATE TYPE enable AS (f1 int, f2 text);
select typname from pg_type where typname ='enable';
drop type enable;


--关键字enable作为数据类型名加双引号，创建成功
drop type if exists "enable";
CREATE TYPE "enable" AS (f1 int, f2 text);
select typname from pg_type where typname ='enable';
drop type "enable";

--关键字enable作为数据类型名加单引号，合理报错
drop type if exists 'enable';
CREATE TYPE 'enable' AS (f1 int, f2 text);
select * from pg_type where typname ='enable';
drop type 'enable';

--关键字enable作为数据类型名加反引号，合理报错
drop type if exists `enable`;
CREATE TYPE `enable` AS (f1 int, f2 text);
select * from pg_type where typname =`enable`;
drop type `enable`;