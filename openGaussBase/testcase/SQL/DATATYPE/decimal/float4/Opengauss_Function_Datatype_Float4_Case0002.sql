-- @testpoint: 插入负浮点数

drop table if exists float4_02;
create table float4_02 (name float4);
insert into float4_02 values (-1212.5);
insert into float4_02 values (-99999.99999);
insert into float4_02 values (-0.00001);
select * from float4_02;
drop table float4_02;
