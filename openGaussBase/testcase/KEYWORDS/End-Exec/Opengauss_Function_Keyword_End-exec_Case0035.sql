--  @testpoint:opengauss关键字end-exec(非保留)，自定义数据类型名为end-exec
--关键字end-exec作为数据类型不带引号，创建成功
drop type if exists end-exec;
CREATE TYPE end-exec AS (f1 int, f2 text);
select typname from pg_type where typname ='end-exec';
drop type end-exec;


--关键字end-exec作为数据类型名加双引号，创建成功
drop type if exists "end-exec";
CREATE TYPE "end-exec" AS (f1 int, f2 text);
select typname from pg_type where typname ='end-exec';
drop type "end-exec";

--关键字end-exec作为数据类型名加单引号，合理报错
drop type if exists 'end-exec';
CREATE TYPE 'end-exec' AS (f1 int, f2 text);
select * from pg_type where typname ='end-exec';
drop type 'end-exec';

--关键字end-exec作为数据类型名加反引号，合理报错
drop type if exists `end-exec`;
CREATE TYPE `end-exec` AS (f1 int, f2 text);
select * from pg_type where typname =`end-exec`;
drop type `end-exec`;