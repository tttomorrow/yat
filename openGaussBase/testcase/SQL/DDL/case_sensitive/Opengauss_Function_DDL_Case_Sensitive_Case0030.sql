--  @testpoint: --查看视图where条件区分大小写
drop view if exists VIEW_2 cascade;
create view VIEW_2 as select * from false_2;
create or replace view VIEW_2 as select * from false_2;
insert into false_2 values (null,null);
select * from view_3,VIEW_2 where VIEW_2.B is null;
select * from view_3,VIEW_2 where view_2.a is null;
select * from view_3,VIEW_2 where VIEW_2.a is null;
select * from view_3 where F=1;
