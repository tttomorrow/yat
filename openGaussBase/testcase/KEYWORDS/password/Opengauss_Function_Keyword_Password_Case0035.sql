--  @testpoint:opengauss关键字password(非保留)，自定义数据类型名为password
--关键字password作为数据类型不带引号，创建成功
drop type if exists password;
CREATE TYPE password AS (f1 int, f2 text);
select typname from pg_type where typname ='password';
drop type password;


--关键字password作为数据类型加双引号，创建成功
drop type if exists "password";
CREATE TYPE "password" AS (f1 int, f2 text);
select typname from pg_type where typname ='password';
drop type "password";

--关键字password作为数据类型加单引号，合理报错
drop type if exists 'password';
CREATE TYPE 'password' AS (f1 int, f2 text);
select * from pg_type where typname ='password';
drop type 'password';

--关键字password作为数据类型加反引号，合理报错
drop type if exists `password`;
CREATE TYPE `password` AS (f1 int, f2 text);
select * from pg_type where typname =`password`;
drop type `password`;