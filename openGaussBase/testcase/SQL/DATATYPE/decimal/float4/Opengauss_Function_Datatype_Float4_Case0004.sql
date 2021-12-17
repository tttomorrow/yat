-- @testpoint: 插入数值超出精度范围，自动截取

drop table if exists float4_04;
create table float4_04 (name float4);
insert into float4_04 values (14165132.9999999999999999999999);
insert into float4_04 values (-14165132.999999999999999999999);
insert into float4_04 values (123.456789123);
insert into float4_04 values (-123.456123789);
select * from float4_04;
drop table float4_04;
