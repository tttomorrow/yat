-- @testpoint: 插入非法空值，合理报错

drop table if exists float4_12;
create table float4_12 (id int,name float8);
insert into float4_12 values (1,' ');
drop table float4_12;