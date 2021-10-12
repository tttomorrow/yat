-- @testpoint: 插入空值

drop table if exists float14;
create table float14 (id int,name float);
insert into float14 values (1,null);
insert into float14 values (2,'');
select * from float14;
drop table float14;