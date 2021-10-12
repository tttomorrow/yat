--  @testpoint:opengauss关键字depth(非保留)，自定义数据类型名为depth
--关键字depth作为数据类型不带引号，创建成功
drop type if exists depth;
CREATE TYPE depth AS (f1 int, f2 text);
select typname from pg_type where typname ='depth';
drop type depth;


--关键字depth作为数据类型加双引号，创建成功
drop type if exists "depth";
CREATE TYPE "depth" AS (f1 int, f2 text);
select typname from pg_type where typname ='depth';
drop type "depth";

--关键字depth作为数据类型加单引号，合理报错
drop type if exists 'depth';
CREATE TYPE 'depth' AS (f1 int, f2 text);


--关键字depth作为数据类型加反引号，合理报错
drop type if exists `depth`;
CREATE TYPE `depth` AS (f1 int, f2 text);
