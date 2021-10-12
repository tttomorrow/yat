--  @testpoint: --创建视图对象为同名的大写视图
select * from view_2;
select * from VIEW_2;
create or replace view view_2 as select * from VIEW_2;
--报错，检测到无限递归
select * from view_2;
drop view if exists view_2 cascade;
--大小写创建与表名相同的view名:报错
create or replace view FALSE_3 AS SELECT * FROM false_3;
select * from FALSE_3;
--报错，提示cannot drop column i of table t because other objects depend on it
ALTER TABLE false_3 drop column a;

select * from false_3;
select * from FALSE_3;
drop view if exists view_1;
--DROP VIEW if exists VIEW_2;
--DROP VIEW if exists FALSE_3;
