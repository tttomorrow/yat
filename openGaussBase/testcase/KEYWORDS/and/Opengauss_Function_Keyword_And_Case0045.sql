-- @testpoint: 表名和列名同时出现关键字and，与dml结合
drop table if exists "and" CASCADE;
create table "and" ("and" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into "and"("and",stu_age) values('wangwu',25);
update "and" set "and"='wujun';
delete from "and";
select * from "and";
drop table if exists "and";