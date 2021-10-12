-- @testpoint: 数字操作函数，正切函数，字符合理报错

--创建测试表并插入数据
drop table if exists tan_T5;
create table tan_T5(f1 char(50),f2 nchar(100),f3 varchar(332),f4 nvarchar2(200));
insert into tan_T5(f1,f2,f3,f4) values ('aa','bb','cc','ee');

select tan(f4) from tan_T5;
select tan(f3) from tan_T5;
select tan(f2) from tan_T5;
select tan(f1) from tan_T5;

----清理环境
drop table if exists tan_T5;