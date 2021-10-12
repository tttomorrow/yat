--  @testpoint:opengauss关键字directory(非保留)，自定义数据类型名为directory
--关键字directory作为数据类型不带引号，创建成功
drop type if exists directory;
CREATE TYPE directory AS (f1 int, f2 text);
select typname from pg_type where typname ='directory';
drop type directory;


--关键字directory作为用户名加双引号，创建成功
drop type if exists "directory";
CREATE TYPE "directory" AS (f1 int, f2 text);
select typname from pg_type where typname ='directory';
drop type "directory";

--关键字directory作为用户名加单引号，合理报错
drop type if exists 'directory';
CREATE TYPE 'directory' AS (f1 int, f2 text);
select * from pg_type where typname ='directory';
drop type 'directory';

--关键字directory作为用户名加反引号，合理报错
drop type if exists `directory`;
CREATE TYPE `directory` AS (f1 int, f2 text);
select * from pg_type where typname =`directory`;
drop type `directory`;