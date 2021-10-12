-- @testpoint: 插入字符串类型，合理报错

drop table if exists float4_05;
create table float4_05 (name float4);
insert into float4_05 values ('123abc');
insert into float4_05 values ('1235ss4563');
insert into float4_05 values ('abc456');
drop table float4_05;