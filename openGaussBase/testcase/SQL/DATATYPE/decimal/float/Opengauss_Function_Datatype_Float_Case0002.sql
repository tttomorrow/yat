-- @testpoint: 不指定精度，插入负浮点数

drop table if exists float02;
create table float02 (name float);
insert into float02 values (-1212.5);
insert into float02 values (-0.0001);
insert into float02 values (-99999.99999);
select * from float02;
drop table float02;
