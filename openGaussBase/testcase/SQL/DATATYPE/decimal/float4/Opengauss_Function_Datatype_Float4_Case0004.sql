-- @testpoint: 插入数值超出精度范围，自动截取
-- @modified at:2020-11-23

drop table if exists float4_04;
create table float4_04 (name float4);
select * from float4_04;
drop table float4_04;
