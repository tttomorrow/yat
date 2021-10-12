--  @testpoint:opengauss关键字eol(非保留)，自定义数据类型名为eol
--关键字eol作为数据类型不带引号，创建成功
drop type if exists eol;
CREATE TYPE eol AS (f1 int, f2 text);
select typname from pg_type where typname ='eol';
drop type eol;


--关键字eol作为数据类型名加双引号，创建成功
drop type if exists "eol";
CREATE TYPE "eol" AS (f1 int, f2 text);
select typname from pg_type where typname ='eol';
drop type "eol";

--关键字eol作为数据类型名加单引号，合理报错
drop type if exists 'eol';
CREATE TYPE 'eol' AS (f1 int, f2 text);
select * from pg_type where typname ='eol';
drop type 'eol';

--关键字eol作为数据类型名加反引号，合理报错
drop type if exists `eol`;
CREATE TYPE `eol` AS (f1 int, f2 text);
select * from pg_type where typname =`eol`;
drop type `eol`;