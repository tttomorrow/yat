-- @testpoint: 数字操作函数，正切函数，与order by/group by结合使用

drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);
select cast(tan(f1) as number(5,2)),cast(tan(f2) as number(5,2))||2 from tan_T1 where tan(tan('11')) <> 1  order by tan(f1);
select cast(tan(f3) as number(5,2)),cast(tan(f1) as number(5,2))||2 from tan_T1 where tan(tan(00)) < 1 group by f3,f1 order by tan(f1);
select cast(tan(f2) as number(5,2)),f3 from tan_T1 group by tan(f2),f3 order by 1;
drop table if exists tan_T1;
