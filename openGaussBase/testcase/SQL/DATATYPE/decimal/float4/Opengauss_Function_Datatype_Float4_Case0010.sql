-- @testpoint: 插入空值

drop table if exists float4_10;
create table float4_10 (id int,name float4);
insert into float4_10 values (1,null);
insert into float4_10 values (2,'');
select * from float4_10;
drop table if exists float4_10;