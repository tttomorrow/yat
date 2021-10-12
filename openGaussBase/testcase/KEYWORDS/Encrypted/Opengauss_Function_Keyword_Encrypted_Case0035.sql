--  @testpoint:opengauss关键字encrypted(非保留)，自定义数据类型名为encrypted
--关键字encrypted作为数据类型不带引号，创建成功
drop type if exists encrypted;
CREATE TYPE encrypted AS (f1 int, f2 text);
select typname from pg_type where typname ='encrypted';
drop type encrypted;


--关键字encrypted作为数据类型名加双引号，创建成功
drop type if exists "encrypted";
CREATE TYPE "encrypted" AS (f1 int, f2 text);
select typname from pg_type where typname ='encrypted';
drop type "encrypted";

--关键字encrypted作为数据类型名加单引号，合理报错
drop type if exists 'encrypted';
CREATE TYPE 'encrypted' AS (f1 int, f2 text);
select * from pg_type where typname ='encrypted';
drop type 'encrypted';

--关键字encrypted作为数据类型名加反引号，合理报错
drop type if exists `encrypted`;
CREATE TYPE `encrypted` AS (f1 int, f2 text);
select * from pg_type where typname =`encrypted`;
drop type `encrypted`;