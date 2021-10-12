-- @testpoint: 插入0值

drop table if exists float13;
create table float13 (name float);
insert into float13 values (0);
insert into float13 values (0);
insert into float13 values (0);
select * from float13;
drop table float13;