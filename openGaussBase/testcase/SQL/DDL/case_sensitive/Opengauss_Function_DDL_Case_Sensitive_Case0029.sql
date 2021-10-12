--  @testpoint: --查看视图字段区分大小写

insert into false_3 values (0,1);
select * from view_3;
select a from view_3;
select A from view_3;
select f from view_3;
select F from view_3;