--  @testpoint:opengauss关键字destroy(非保留)，自定义数据类型名为destroy
--关键字destroy作为数据类型不带引号，创建成功
drop type if exists destroy;
CREATE TYPE destroy AS (f1 int, f2 text);
select typname from pg_type where typname ='destroy';
drop type destroy;


--关键字destroy作为数据类型名加双引号，创建成功
drop type if exists "destroy";
CREATE TYPE "destroy" AS (f1 int, f2 text);
select typname from pg_type where typname ='destroy';
drop type "destroy";

--关键字destroy作为数据类型名加单引号，合理报错
drop type if exists 'destroy';
CREATE TYPE 'destroy' AS (f1 int, f2 text);
select * from pg_type where typname ='destroy';
drop type 'destroy';

--关键字destroy作为数据类型名加反引号，合理报错
drop type if exists `destroy`;
CREATE TYPE `destroy` AS (f1 int, f2 text);
select * from pg_type where typname =`destroy`;
drop type `destroy`;