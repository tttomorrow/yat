--  @testpoint: --查看视图时子查询区分大小写
drop view if exists VIEW_2 cascade;
create view VIEW_2 as select * from false_2;
insert into false_2 values(1,1);
select * from view_3 where f in (select A from view_2);
select * from view_3 where f in (select B from view_2);
select * from view_3 where f in (select b from view_2);