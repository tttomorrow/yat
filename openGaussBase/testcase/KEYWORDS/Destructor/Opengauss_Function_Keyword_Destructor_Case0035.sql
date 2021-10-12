--  @testpoint:opengauss关键字destructor(非保留)，自定义数据类型名为destructor
--关键字destructor作为数据类型不带引号，创建成功
drop type if exists destructor;
CREATE TYPE destructor AS (f1 int, f2 text);
select typname from pg_type where typname ='destructor';
drop type destructor;


--关键字destructor作为数据类型名加双引号，创建成功
drop type if exists "destructor";
CREATE TYPE "destructor" AS (f1 int, f2 text);
select typname from pg_type where typname ='destructor';
drop type "destructor";

--关键字destructor作为数据类型名加单引号，合理报错
drop type if exists 'destructor';
CREATE TYPE 'destructor' AS (f1 int, f2 text);
select * from pg_type where typname ='destructor';
drop type 'destructor';

--关键字destructor作为数据类型名加反引号，合理报错
drop type if exists `destructor`;
CREATE TYPE `destructor` AS (f1 int, f2 text);
select * from pg_type where typname =`destructor`;
drop type `destructor`;