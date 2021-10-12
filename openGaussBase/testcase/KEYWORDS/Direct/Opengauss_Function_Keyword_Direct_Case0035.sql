--  @testpoint:opengauss关键字direct(非保留)，自定义数据类型名为direct
--关键字direct作为数据类型不带引号，创建成功
drop type if exists direct;
CREATE TYPE direct AS (f1 int, f2 text);
select typname from pg_type where typname ='direct';
drop type direct;


--关键字direct作为用户名加双引号，创建成功
drop type if exists "direct";
CREATE TYPE "direct" AS (f1 int, f2 text);
select typname from pg_type where typname ='direct';
drop type "direct";

--关键字direct作为用户名加单引号，合理报错
drop type if exists 'direct';
CREATE TYPE 'direct' AS (f1 int, f2 text);
select * from pg_type where typname ='direct';
drop type 'direct';

--关键字direct作为用户名加反引号，合理报错
drop type if exists `direct`;
CREATE TYPE `direct` AS (f1 int, f2 text);
select * from pg_type where typname =`direct`;
drop type `direct`;