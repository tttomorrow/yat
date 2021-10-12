
--  @testpoint:opengauss关键字delta(非保留)，自定义数据类型名为delta
--关键字delta作为数据类型不带引号，创建成功
drop type if exists delta;
CREATE TYPE delta AS (f1 int, f2 text);
select typname from pg_type where typname ='delta';
drop type delta;


--关键字delta作为数据类型名加双引号，创建成功
drop type if exists "delta";
CREATE TYPE "delta" AS (f1 int, f2 text);
select typname from pg_type where typname ='delta';
drop type "delta";

--关键字delta作为数据类型名加单引号，合理报错
drop type if exists 'delta';
CREATE TYPE 'delta' AS (f1 int, f2 text);
select typname from pg_type where typname ='delta';
drop type 'delta';

--关键字delta作为数据类型名加反引号，合理报错
drop type if exists `delta`;
CREATE TYPE `delta` AS (f1 int, f2 text);
select typname from pg_type where typname =`delta`;
drop type `delta`;
