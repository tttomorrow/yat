--  @testpoint:opengauss关键字distinct(保留)，自定义数据类型名为distinct
--关键字distinct作为数据类型不带引号，创建失败
drop type if exists distinct;
CREATE TYPE distinct AS (f1 int, f2 text);

--关键字distinct作为数据类型加双引号，创建成功
drop type if exists "distinct";
CREATE TYPE "distinct" AS (f1 int, f2 text);
select typname from pg_type where typname ='distinct';
drop type "distinct";

--关键字distinct作为数据类型加单引号，合理报错
drop type if exists 'distinct';
CREATE TYPE 'distinct' AS (f1 int, f2 text);


--关键字distinct作为数据类型加反引号，合理报错
drop type if exists `distinct`;
CREATE TYPE `distinct` AS (f1 int, f2 text);
