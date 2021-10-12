-- @testpoint: 插入bool类型，合理报错

drop table if exists float4_06;
create table float4_06 (name float4);
insert into float4_06 values (false);
insert into float4_06 values (true);
drop table float4_06;