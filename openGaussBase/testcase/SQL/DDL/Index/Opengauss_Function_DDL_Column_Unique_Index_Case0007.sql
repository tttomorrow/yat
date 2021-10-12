-- @testpoint: 普通列存表，增加表字段(单字段)主键约束，部分测试点合理报错

--测试点1：创建普通列存表，表中存在数据，数据为唯一且非空
drop table if exists columns_tab07;
create table columns_tab07(id int) with(orientation=column);
insert into columns_tab07 values(generate_series(1,1000));

--修改字段主键约束
alter table columns_tab07 add primary key(id);

--查看是否存在唯一索引
select indisunique from pg_index where indexrelid = (select oid from pg_class where relname = 'columns_tab07_pkey');

--删除表
drop table columns_tab07 cascade;


--测试点2：创建普通列存表，表中存在数据，数据为唯一且有空值
drop table if exists columns_tab07;
create table columns_tab07(id int) with(orientation=column);
insert into columns_tab07 values(generate_series(1,1000));
insert into columns_tab07 values(null),(null),(null);

--修改字段主键约束,合理报错
alter table columns_tab07 add primary key(id);

--删除表
drop table columns_tab07 cascade;


--测试点3：创建普通列存表，表中存在数据，数据不唯一且非空
drop table if exists columns_tab07;
create table columns_tab07(id int) with(orientation=column);
insert into columns_tab07 values(generate_series(1,100));
insert into columns_tab07 values(generate_series(1,100));
insert into columns_tab07 values(generate_series(1,100));

--修改字段主键约束，合理报错
alter table columns_tab07 add primary key(id);

--删除表
drop table columns_tab07 cascade;


--测试点4：创建普通列存表，表中存在数据，数据不唯一且有空值
drop table if exists columns_tab07;
create table columns_tab07(id int) with(orientation=column);
insert into columns_tab07 values(generate_series(1,100));
insert into columns_tab07 values(null),(null),(null);
insert into columns_tab07 values(generate_series(1,100));

--修改字段主键约束，合理报错
alter table columns_tab07 add primary key(id);

--删除表
drop table columns_tab07 cascade;


--测试点5：创建普通列存表，表中不存在数据，添加主键约束，插入数据
drop table if exists columns_tab07;
create table columns_tab07(id int) with(orientation=column);

--修改字段主键约束
alter table columns_tab07 add primary key(id);

--插入数据
insert into columns_tab07 values(generate_series(1,1000));

--再次插入已存在数据，合理报错
insert into columns_tab07 values(generate_series(1,1000));

--查看数据
select count(*) from columns_tab07 where id=1;

--删除表
drop table columns_tab07 cascade;
