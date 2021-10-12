--  @testpoint:opengauss关键字pctfree(非保留)，自定义数据类型名为pctfree
--关键字pctfree作为数据类型不带引号，创建成功
drop type if exists pctfree;
CREATE TYPE pctfree AS (f1 int, f2 text);
select typname from pg_type where typname ='pctfree';
drop type pctfree;


--关键字pctfree作为数据类型加双引号，创建成功
drop type if exists "pctfree";
CREATE TYPE "pctfree" AS (f1 int, f2 text);
select typname from pg_type where typname ='pctfree';
drop type "pctfree";

--关键字pctfree作为数据类型加单引号，合理报错
drop type if exists 'pctfree';
CREATE TYPE 'pctfree' AS (f1 int, f2 text);
select * from pg_type where typname ='pctfree';
drop type 'pctfree';

--关键字pctfree作为数据类型加反引号，合理报错
drop type if exists `pctfree`;
CREATE TYPE `pctfree` AS (f1 int, f2 text);
select * from pg_type where typname =`pctfree`;
drop type `pctfree`;