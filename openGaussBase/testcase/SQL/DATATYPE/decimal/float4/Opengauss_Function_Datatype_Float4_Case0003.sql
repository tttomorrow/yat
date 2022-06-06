-- @testpoint: 插入整数

drop table if exists float4_03;
create table float4_03 (name float4);
insert into float4_03 values (12122);
insert into float4_03 values (99999999999);
insert into float4_03 values (-12122);
insert into float4_03 values (-99999999999);
select * from float4_03;
drop table float4_03;
