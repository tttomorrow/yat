-- @testpoint: 插入非法空值，合理报错

drop table if exists float4_08;
create table float4_08 (id int,name float4);
insert into float4_08 values (1,' ');
drop table float4_08;