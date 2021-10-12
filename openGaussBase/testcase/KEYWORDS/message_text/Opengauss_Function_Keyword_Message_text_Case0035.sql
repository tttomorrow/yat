--  @testpoint:opengauss关键字message_text(非保留)，自定义数据类型名为explain
--关键字explain作为数据类型不带引号，创建成功
drop type if exists message_text;
CREATE TYPE message_text AS (f1 int, f2 text);
select typname from pg_type where typname ='message_text';
drop type message_text;


--关键字explain作为数据类型加双引号，创建成功
drop type if exists "message_text";
CREATE TYPE "message_text" AS (f1 int, f2 text);
select typname from pg_type where typname ='message_text';
drop type "message_text";

--关键字explain作为数据类型加单引号，合理报错
drop type if exists 'message_text';
CREATE TYPE 'message_text' AS (f1 int, f2 text);
select * from pg_type where typname ='message_text';
drop type 'message_text';

--关键字explain作为数据类型加反引号，合理报错
drop type if exists `message_text`;
CREATE TYPE `message_text` AS (f1 int, f2 text);
select * from pg_type where typname =`message_text`;
drop type `message_text`;