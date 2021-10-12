-- @testpoint: 列存本地临时表，增加表字段(单字段)唯一约束，部分测试点合理报错

--测试点1：创建列存本地临时表，表中存在数据，数据为唯一且非空
drop table if exists columns_local_tab14;
create local temp table columns_local_tab14(id int) with(orientation=column);
insert into columns_local_tab14 values(generate_series(1,1000));

--修改字段唯一约束
alter table columns_local_tab14 add constraint const14 unique(id);

--删除表
drop table columns_local_tab14 cascade;


--测试点2：创建列存本地临时表，表中存在数据，数据为唯一且有空值
drop table if exists columns_local_tab14;
create local temp table columns_local_tab14(id int) with(orientation=column);
insert into columns_local_tab14 values(generate_series(1,1000));
insert into columns_local_tab14 values(null),(null),(null);

--修改字段唯一约束
alter table columns_local_tab14 add constraint const14 unique(id);

--删除表
drop table columns_local_tab14 cascade;


--测试点3：创建列存本地临时表，表中存在数据，数据不唯一且非空
drop table if exists columns_local_tab14;
create local temp table columns_local_tab14(id int) with(orientation=column);
insert into columns_local_tab14 values(generate_series(1,100));
insert into columns_local_tab14 values(generate_series(1,100));
insert into columns_local_tab14 values(generate_series(1,100));

--修改字段唯一约束，合理报错
alter table columns_local_tab14 add constraint const14 unique(id);

--删除表
drop table columns_local_tab14 cascade;


--测试点4：创建列存本地临时表，表中存在数据，数据不唯一且有空值
drop table if exists columns_local_tab14;
create local temp table columns_local_tab14(id int) with(orientation=column);
insert into columns_local_tab14 values(generate_series(1,100));
insert into columns_local_tab14 values(null),(null),(null);
insert into columns_local_tab14 values(generate_series(1,100));

--修改字段唯一约束，合理报错
alter table columns_local_tab14 add constraint const14 unique(id);

--删除表
drop table columns_local_tab14 cascade;


--测试点5：创建列存本地临时表，表中不存在数据，添加唯一约束，插入数据
drop table if exists columns_local_tab14;
create local temp table columns_local_tab14(id int) with(orientation=column);

--修改字段唯一约束
alter table columns_local_tab14 add constraint const14 unique(id);

--插入数据
insert into columns_local_tab14 values(generate_series(1,1000));

--再次插入已存在数据，合理报错
insert into columns_local_tab14 values(generate_series(1,1000));

--查看数据
select count(*) from columns_local_tab14 where id=1;

--删除表
drop table columns_local_tab14 cascade;
