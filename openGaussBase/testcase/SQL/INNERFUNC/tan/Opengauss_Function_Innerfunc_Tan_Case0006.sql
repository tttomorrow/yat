-- @testpoint: 数字操作函数，正切函数，参数为''或者参数为null

drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);

select tan(null) from tan_T1;
select tan(cast(null as number)) from tan_T1;
select tan(cast('' as number)) from tan_T1;
drop table if exists tan_T1;

