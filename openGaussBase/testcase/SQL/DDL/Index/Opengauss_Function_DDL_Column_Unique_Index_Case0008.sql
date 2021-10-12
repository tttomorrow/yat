-- @testpoint: 普通列存表，增加表字段(单字段)唯一约束，部分测试点合理报错

--测试点1：创建普通列存表，表中存在数据，数据为唯一且非空
drop table if exists columns_tab08;
create table columns_tab08(id int) with(orientation=column);
insert into columns_tab08 values(generate_series(1,1000));

--修改字段主键约束
alter table columns_tab08 add constraint const8 unique(id);

--删除表
drop table columns_tab08 cascade;


--测试点2：创建普通列存表，表中存在数据，数据为唯一且有空值
drop table if exists columns_tab08;
create table columns_tab08(id int) with(orientation=column);
insert into columns_tab08 values(generate_series(1,1000));
insert into columns_tab08 values(null),(null),(null);

--修改字段主键约束
alter table columns_tab08 add constraint const8 unique(id);

--删除表
drop table columns_tab08 cascade;


--测试点3：创建普通列存表，表中存在数据，数据不唯一且非空
drop table if exists columns_tab08;
create table columns_tab08(id int) with(orientation=column);
insert into columns_tab08 values(generate_series(1,100));
insert into columns_tab08 values(generate_series(1,100));
insert into columns_tab08 values(generate_series(1,100));

--修改字段主键约束，合理报错
alter table columns_tab08 add constraint const8 unique(id);

--删除表
drop table columns_tab08 cascade;


--测试点4：创建普通列存表，表中存在数据，数据不唯一且有空值
drop table if exists columns_tab08;
create table columns_tab08(id int) with(orientation=column);
insert into columns_tab08 values(generate_series(1,100));
insert into columns_tab08 values(null),(null),(null);
insert into columns_tab08 values(generate_series(1,100));

--修改字段主键约束，合理报错
alter table columns_tab08 add constraint const8 unique(id);

--删除表
drop table columns_tab08 cascade;


--测试点5：创建普通列存表，表中不存在数据，添加唯一约束，插入数据
drop table if exists columns_tab08;
create table columns_tab08(id int) with(orientation=column);

--修改字段主键约束
alter table columns_tab08 add constraint const8 unique(id);

--插入数据
insert into columns_tab08 values(generate_series(1,100));
insert into columns_tab08 values(null),(null),(null);
insert into columns_tab08 values(generate_series(101,200));

--再次插入已存在数据，合理报错
insert into columns_tab08 values(generate_series(1,100));

--查看数据
select count(*) from columns_tab08 where id=1;

--删除表
drop table columns_tab08 cascade;