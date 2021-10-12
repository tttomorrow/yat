-- @testpoint: 普通列存表，创建(多字段)唯一索引，部分测试点合理报错

--测试点1：创建普通列存表，表中存在数据，数据为唯一且非空
drop table if exists columns_tab12;
create table columns_tab12(id1 int,id2 int) with(orientation=column);
insert into columns_tab12 values(generate_series(1,1000),generate_series(1,1000));

--创建唯一索引
create unique index column_index12 on columns_tab12 using btree(id1,id2);

--删除表
drop table columns_tab12 cascade;


--测试点2：创建普通列存表，表中存在数据，数据为唯一且有空值
drop table if exists columns_tab12;
create table columns_tab12(id1 int,id2 int) with(orientation=column);
insert into columns_tab12 values(generate_series(1,1000),generate_series(1,1000));
insert into columns_tab12 values(null,null),(null,''),('',null);

--创建唯一索引
create unique index column_index12 on columns_tab12 using btree(id1,id2);

--删除表
drop table columns_tab12 cascade;


--测试点3：创建普通列存表，表中存在数据，数据不唯一且非空
drop table if exists columns_tab12;
create table columns_tab12(id1 int,id2 int) with(orientation=column);
insert into columns_tab12 values(generate_series(1,100),generate_series(1,100));
insert into columns_tab12 values(generate_series(1,100),generate_series(1,100));
insert into columns_tab12 values(generate_series(1,100),generate_series(1,100));

--创建唯一索引，合理报错
create unique index column_index12 on columns_tab12 using btree(id1,id2);

--删除表
drop table columns_tab12 cascade;


--测试点4：创建普通列存表，表中存在数据，数据不唯一且有空值
drop table if exists columns_tab12;
create table columns_tab12(id1 int,id2 int) with(orientation=column);
insert into columns_tab12 values(generate_series(1,100),generate_series(1,100));
insert into columns_tab12 values(null,''),(null,null),('',null);
insert into columns_tab12 values(generate_series(1,100),generate_series(1,100));

--创建唯一索引，合理报错
create unique index column_index12 on columns_tab12 using btree(id1,id2);

--删除表
drop table columns_tab12 cascade;


--测试点5：创建普通列存表，表中不存在数据，添加唯一索引，插入数据
drop table if exists columns_tab12;
create table columns_tab12(id1 int,id2 int) with(orientation=column);

--创建唯一索引
create unique index column_index12 on columns_tab12 using btree(id1,id2);

--插入正常数据
insert into columns_tab12 values(generate_series(1,1000),generate_series(1,1000));

--再次插入已存在的数据，合理报错
insert into columns_tab12 values(generate_series(1,1000),generate_series(1,1000));

--查看数据
select count(*) from columns_tab12 where id1=1;

--删除表
drop table columns_tab12 cascade;