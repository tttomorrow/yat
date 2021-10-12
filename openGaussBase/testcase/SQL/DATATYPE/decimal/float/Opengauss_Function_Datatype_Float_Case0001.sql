-- @testpoint: 不指定精度，插入正浮点数

drop table if exists float01;
create table float01 (name float);
insert into float01 values (120.123);
insert into float01 values (0.001);
insert into float01 values (99999.99999);
select * from float01;
drop table float01;