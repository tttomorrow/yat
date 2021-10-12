-- @testpoint: 插入浮点数，四舍五入取整

drop table if exists integer12;
create table integer12 (name integer);
insert into integer12 values (122.3340);
insert into integer12 values (0.0000001);
insert into integer12 values (-122.3340);
insert into integer12 values (-0.0000001);
select * from integer12;
drop table integer12;