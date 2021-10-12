-- @testpoint: 列存本地临时表，增加表字段(多字段)主键约束，部分测试点合理报错

--测试点1：创建列存本地临时表，表中存在数据，数据为唯一且非空
drop table if exists columns_local_tab15;
create local temp table columns_local_tab15(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab15 values(generate_series(1,1000),generate_series(1,1000));

--修改字段主键约束
alter table columns_local_tab15 add primary key(id1,id2);

--删除表
drop table columns_local_tab15 cascade;


--测试点2：创建列存本地临时表，表中存在数据，数据为唯一且有空值
drop table if exists columns_local_tab15;
create local temp table columns_local_tab15(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab15 values(generate_series(1,1000),generate_series(1,1000));
insert into columns_local_tab15 values(null,''),(null,null),('',null);

--修改字段主键约束,合理报错
alter table columns_local_tab15 add primary key(id1,id2);

--删除表
drop table columns_local_tab15 cascade;


--测试点3：创建列存本地临时表，表中存在数据，数据不唯一且非空
drop table if exists columns_local_tab15;
create local temp table columns_local_tab15(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab15 values(generate_series(1,100),generate_series(1,100));
insert into columns_local_tab15 values(generate_series(1,100),generate_series(1,100));
insert into columns_local_tab15 values(generate_series(1,100),generate_series(1,100));

--修改字段主键约束，合理报错
alter table columns_local_tab15 add primary key(id1,id2);

--删除表
drop table columns_local_tab15 cascade;


--测试点4：创建列存本地临时表，表中存在数据，数据不唯一且有空值
drop table if exists columns_local_tab15;
create local temp table columns_local_tab15(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab15 values(generate_series(1,100),generate_series(1,100));
insert into columns_local_tab15 values(null,''),('',null),(null,null);
insert into columns_local_tab15 values(generate_series(1,100),generate_series(1,100));

--修改字段主键约束，合理报错
alter table columns_local_tab15 add primary key(id1,id2);

--删除表
drop table columns_local_tab15 cascade;


--测试点5：创建列存本地临时表，表中不存在数据，添加主键约束，插入数据
drop table if exists columns_local_tab15;
create local temp table columns_local_tab15(id1 int,id2 int) with(orientation=column);

--修改字段主键约束
alter table columns_local_tab15 add primary key(id1,id2);

--插入数据
insert into columns_local_tab15 values(generate_series(1,1000),generate_series(1,1000));

--再次插入已存在数据，合理报错
insert into columns_local_tab15 values(generate_series(1,1000),generate_series(1,1000));

--查看数据
select count(*) from columns_local_tab15 where id1=1;

--删除表
drop table columns_local_tab15 cascade;
