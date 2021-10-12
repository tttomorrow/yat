-- @testpoint: 列存本地临时表，创建(单字段)唯一索引，部分测试点合理报错

--测试点1：创建列存本地临时表，表中存在数据，数据为唯一且非空
drop table if exists columns_local_tab17;
create local temp table columns_local_tab17(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab17 values(generate_series(1,1000));

--创建唯一索引
create unique index column_index17 on columns_local_tab17 using btree(id1);

--删除表
drop table columns_local_tab17 cascade;


--测试点2：创建列存本地临时表，表中存在数据，数据为唯一且有空值
drop table if exists columns_local_tab17;
create local temp table columns_local_tab17(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab17 values(generate_series(1,1000));
insert into columns_local_tab17 values(null),(null),(null);

--创建唯一索引
create unique index column_index17 on columns_local_tab17 using btree(id1);

--删除表
drop table columns_local_tab17 cascade;


--测试点3：创建列存本地临时表，表中存在数据，数据不唯一且非空
drop table if exists columns_local_tab17;
create local temp table columns_local_tab17(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab17 values(generate_series(1,100));
insert into columns_local_tab17 values(generate_series(1,100));
insert into columns_local_tab17 values(generate_series(1,100));

--创建唯一索引，合理报错
create unique index column_index17 on columns_local_tab17 using btree(id1);

--删除表
drop table columns_local_tab17 cascade;


--测试点4：创建列存本地临时表，表中存在数据，数据不唯一且有空值
drop table if exists columns_local_tab17;
create local temp table columns_local_tab17(id1 int,id2 int) with(orientation=column);
insert into columns_local_tab17 values(generate_series(1,100));
insert into columns_local_tab17 values(null),(null),(null);
insert into columns_local_tab17 values(generate_series(1,100));

--创建唯一索引，合理报错
create unique index column_index17 on columns_local_tab17 using btree(id1);

--删除表
drop table columns_local_tab17 cascade;


--测试点5：创建列存本地临时表，表中不存在数据，添加唯一索引，插入数据
drop table if exists columns_local_tab17;
create local temp table columns_local_tab17(id1 int,id2 int) with(orientation=column);

--创建唯一索引
create unique index column_index17 on columns_local_tab17 using btree(id1);

--插入正常数据
insert into columns_local_tab17 values(generate_series(1,1000));

--再次插入已存在的数据，合理报错
insert into columns_local_tab17 values(generate_series(1,1000));

--查看数据
select count(*) from columns_local_tab17 where id1=1;

--删除表
drop table columns_local_tab17 cascade;
