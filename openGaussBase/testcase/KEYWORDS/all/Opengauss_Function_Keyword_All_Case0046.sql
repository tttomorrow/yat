-- @testpoint: 表名和列名同时出现关键字all，与dml结合
drop table if exists "all";
create table "all" ("all" char(20),stu_age int,sex char(10),score int,address char(10));
insert into "all" ("all",stu_age)values('zhangsan',20);
update "all" set "all"='lisi';
delete from "all" where "all"='lisi';
select * from "all";
drop table if exists "all";