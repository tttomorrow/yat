--  @testpoint:opengauss关键字deterministic(非保留)，自定义数据类型名为deterministic
--关键字deterministic作为数据类型不带引号，创建成功
drop type if exists deterministic;
CREATE TYPE deterministic AS (f1 int, f2 text);
select typname from pg_type where typname ='deterministic';
drop type deterministic;


--关键字deterministic作为数据类型名加双引号，创建成功
drop type if exists "deterministic";
CREATE TYPE "deterministic" AS (f1 int, f2 text);
select typname from pg_type where typname ='deterministic';
drop type "deterministic";

--关键字deterministic作为数据类型名加单引号，合理报错
drop type if exists 'deterministic';
CREATE TYPE 'deterministic' AS (f1 int, f2 text);
select * from pg_type where typname ='deterministic';
drop type 'deterministic';

--关键字deterministic作为数据类型名加反引号，合理报错
drop type if exists `deterministic`;
CREATE TYPE `deterministic` AS (f1 int, f2 text);
select * from pg_type where typname =`deterministic`;
drop type `deterministic`;