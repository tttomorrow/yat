-- @testpoint: 表名和列名同时出现关键字all,带引号
drop table if exists "all";
create table "all" ("all" char(20),stu_age int,sex char(10),score int,address char(10));
drop table if exists "all";