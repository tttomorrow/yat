-- @testpoint: 插入0值

drop table if exists float4_09;
create table float4_09 (name float4);
insert into float4_09 values (0);
insert into float4_09 values (0);
insert into float4_09 values (0);
select * from float4_09;
drop table float4_09;