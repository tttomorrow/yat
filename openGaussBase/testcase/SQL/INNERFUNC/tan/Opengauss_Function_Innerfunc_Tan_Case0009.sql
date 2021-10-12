-- @testpoint: 数字操作函数，正切函数，与||结合

drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);
select cast(tan(1) as number(5,2))||'abc' from sys_dummy;
select cast(tan(1||2+1)as number(5,2)) from sys_dummy;
select cast(tan(f1||f2||f3)as number(5,2)) from tan_T1;
select * from tan_T1 where tan(f1)+1|| '2' = f2;
select concat(cast(tan(1)as number(5,2)),'abc') from sys_dummy;
drop table if exists tan_T1;
