-- @testpoint: 插入正浮点数

drop table if exists float4_01;
create table float4_01 (name float4);
insert into float4_01 values (120.123);
insert into float4_01 values (99999.99999);
insert into float4_01 values (0.0001);
select * from float4_01;
drop table float4_01;