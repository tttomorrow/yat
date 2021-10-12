--  @testpoint:opengauss关键字distribution(非保留)，自定义数据类型名为distribution
--关键字distribution作为数据类型不带引号，创建成功
drop type if exists distribution;
CREATE TYPE distribution AS (f1 int, f2 text);
select typname from pg_type where typname ='distribution';
drop type distribution;


--关键字distribution作为用户名加双引号，创建成功
drop type if exists "distribution";
CREATE TYPE "distribution" AS (f1 int, f2 text);
select typname from pg_type where typname ='distribution';
drop type "distribution";

--关键字distribution作为用户名加单引号，合理报错
drop type if exists 'distribution';
CREATE TYPE 'distribution' AS (f1 int, f2 text);
select * from pg_type where typname ='distribution';
drop type 'distribution';

--关键字distribution作为用户名加反引号，合理报错
drop type if exists `distribution`;
CREATE TYPE `distribution` AS (f1 int, f2 text);
select * from pg_type where typname =`distribution`;
drop type `distribution`;