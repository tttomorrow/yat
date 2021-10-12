--  @testpoint:创建枚举类型，结合表使用查询
--创建枚举类型
drop type if exists  week cascade;
create type week as enum('Sun','Mon','Tues','Wed','Thur','Fri','Sat');
--建表
drop table if exists duty;
create table duty(person text,weekday week);
--插入数据，输入值在枚举类型中
insert into duty values('April','Sun');
insert into duty values('Harris','Mon');
insert into duty values('Dave','Wed');
--插入数据，输入值不在枚举类型中，合理报错
insert into duty values('Dave','Wed1');
--查询
select * from duty;
--结合聚集函数查询
select min(weekday),max(weekday) from duty;
--删除表
drop table if exists duty;
--删除类型
drop type if exists  week;