--  @testpoint:opengauss关键字delimiter(非保留)，自定义数据类型名为delimiter
--关键字delimiter作为数据类型不带引号，创建成功
drop type if exists delimiter;
CREATE TYPE delimiter AS (f1 int, f2 text);
select typname from pg_type where typname ='delimiter';
drop type delimiter;


--关键字delimiter作为用户名加双引号，创建成功
drop type if exists "delimiter";
CREATE TYPE "delimiter" AS (f1 int, f2 text);
select typname from pg_type where typname ='delimiter';
drop type "delimiter";

--关键字delimiter作为用户名加单引号，合理报错
drop type if exists 'delimiter';
CREATE TYPE 'delimiter' AS (f1 int, f2 text);
select typname from pg_type where typname ='delimiter';
drop type 'delimiter';

--关键字delimiter作为用户名加反引号，合理报错
drop type if exists `delimiter`;
CREATE TYPE `delimiter` AS (f1 int, f2 text);
select typname from pg_type where typname =`delimiter`;
drop type `delimiter`;
