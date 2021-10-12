--  @testpoint: --查看视图区分大小写

drop table if exists false_3 cascade;
create table false_3 (A int,f int);
insert into false_3 values(22,33);

create or replace view view_3 as select * from false_3;

select * from VIEW_3;
select * from view_3;