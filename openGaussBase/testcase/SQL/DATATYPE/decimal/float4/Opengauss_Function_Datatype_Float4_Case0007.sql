-- @testpoint: 插入指数形式值

drop table if exists float4_07;
create table float4_07 (name float4);
insert into float4_07 values (exp(33));
insert into float4_07 values (exp(12.34));
insert into float4_07 values (exp(-15));
insert into float4_07 values (exp(-12.34));
select * from float4_07;
drop table float4_07;