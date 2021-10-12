--  @testpoint:opengauss关键字encoding(非保留)，自定义数据类型名为encoding
--关键字encoding作为数据类型不带引号，创建成功
drop type if exists encoding;
CREATE TYPE encoding AS (f1 int, f2 text);
select typname from pg_type where typname ='encoding';
drop type encoding;


--关键字encoding作为数据类型名加双引号，创建成功
drop type if exists "encoding";
CREATE TYPE "encoding" AS (f1 int, f2 text);
select typname from pg_type where typname ='encoding';
drop type "encoding";

--关键字encoding作为数据类型名加单引号，合理报错
drop type if exists 'encoding';
CREATE TYPE 'encoding' AS (f1 int, f2 text);
select * from pg_type where typname ='encoding';
drop type 'encoding';

--关键字encoding作为数据类型名加反引号，合理报错
drop type if exists `encoding`;
CREATE TYPE `encoding` AS (f1 int, f2 text);
select * from pg_type where typname =`encoding`;
drop type `encoding`;