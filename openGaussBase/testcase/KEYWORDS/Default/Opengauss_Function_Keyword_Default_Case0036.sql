--  @testpoint:opengauss关键字default(保留)，自定义数据类型名为default
--关键字default作为数据类型不带引号，创建失败
drop type if exists default;
CREATE TYPE default AS (f1 int, f2 text);



--关键字default作为数据类型加双引号，创建成功
drop type if exists "default";
CREATE TYPE "default" AS (f1 int, f2 text);
select typname from pg_type where typname ='default';
drop type "default";

--关键字default作为数据类型加单引号，合理报错
drop type if exists 'default';
CREATE TYPE 'default' AS (f1 int, f2 text);


--关键字default作为数据类型加反引号，合理报错
drop type if exists `default`;
CREATE TYPE `default` AS (f1 int, f2 text);
