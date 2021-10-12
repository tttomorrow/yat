--  @testpoint:opengauss关键字document(非保留)，自定义数据类型名为document
--关键字document作为数据类型不带引号，创建成功
drop type if exists document;
CREATE TYPE document AS (f1 int, f2 text);
select typname from pg_type where typname ='document';
drop type document;


--关键字document作为数据类型加双引号，创建成功
drop type if exists "document";
CREATE TYPE "document" AS (f1 int, f2 text);
select typname from pg_type where typname ='document';
drop type "document";

--关键字document作为数据类型加单引号，合理报错
drop type if exists 'document';
CREATE TYPE 'document' AS (f1 int, f2 text);
select * from pg_type where typname ='document';
drop type 'document';

--关键字document作为数据类型加反引号，合理报错
drop type if exists `document`;
CREATE TYPE `document` AS (f1 int, f2 text);
select * from pg_type where typname =`document`;
drop type `document`;