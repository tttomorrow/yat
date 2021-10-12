-- @testpoint: 数字操作函数，正切函数，数值类型 整数

--创建测试表并插入数据
drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);
select tan(f1),tan(f2),tan(f3),tan(f4),tan(f5) from tan_T1;

--清理环境
drop table if exists tan_T1;