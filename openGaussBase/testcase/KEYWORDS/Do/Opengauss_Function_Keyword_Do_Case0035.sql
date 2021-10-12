--  @testpoint:opengauss关键字do(保留)，自定义数据类型名为do
--关键字do作为数据类型不带引号，创建失败
drop type if exists do;
CREATE TYPE do AS (f1 int, f2 text);

--关键字do作为数据类型加双引号，创建成功
drop type if exists "do";
CREATE TYPE "do" AS (f1 int, f2 text);
select typname from pg_type where typname ='do';
drop type "do";

--关键字do作为数据类型加单引号，合理报错
drop type if exists 'do';
CREATE TYPE 'do' AS (f1 int, f2 text);


--关键字do作为数据类型加反引号，合理报错
drop type if exists `do`;
CREATE TYPE `do` AS (f1 int, f2 text);