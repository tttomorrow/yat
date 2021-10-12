--  @testpoint:opengauss关键字delimiters(非保留)，自定义数据类型名为delimiters
--关键字delimiters作为数据类型不带引号，创建成功
drop type if exists delimiters;
CREATE TYPE delimiters AS (f1 int, f2 text);
select typname from pg_type where typname ='delimiters';
drop type delimiters;


--关键字delimiters作为数据类型名加双引号，创建成功
drop type if exists "delimiters";
CREATE TYPE "delimiters" AS (f1 int, f2 text);
select typname from pg_type where typname ='delimiters';
drop type "delimiters";

--关键字delimiters作为数据类型名加单引号，合理报错
drop type if exists 'delimiters';
CREATE TYPE 'delimiters' AS (f1 int, f2 text);
select typname from pg_type where typname ='delimiters';
drop type 'delimiters';

--关键字delimiters作为数据类型名加反引号，合理报错
drop type if exists `delimiters`;
CREATE TYPE `delimiters` AS (f1 int, f2 text);
select typname from pg_type where typname =`delimiters`;
drop type `delimiters`;
