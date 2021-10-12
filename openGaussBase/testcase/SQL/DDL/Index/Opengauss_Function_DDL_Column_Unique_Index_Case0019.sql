-- @testpoint: 列存范围分区表，创建唯一索引，部分测试点合理报错

--测试点1：创建列存范围分区表，表中存在数据，数据为唯一且非空
drop table if exists column_part_tab19;
create table column_part_tab19(id int,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--创建唯一索引
create unique index column_index19 on column_part_tab19 using btree(id) local;

--删除表
drop table column_part_tab19 cascade;


--测试点2：创建列存范围分区表，表中存在数据，数据为唯一且有空值
drop table if exists column_part_tab19;
create table column_part_tab19(id int,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));
insert into column_part_tab19 values(null,null),('',null),(null,'');

--创建唯一索引,指定索引分区的名称
create unique index column_index19 on column_part_tab19 using btree(id) local (partition idx_p1,partition idx_p2,partition idx_p3,partition idx_p4,partition idx_p5);

--删除表
drop table column_part_tab19 cascade;


--测试点3：创建列存范围分区表，表中存在数据，数据不唯一且非空
drop table if exists column_part_tab19;
create table column_part_tab19(id int,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--创建唯一索引，合理报错
create unique index column_index19 on column_part_tab19 using btree(id) local;

--删除表
drop table column_part_tab19 cascade;


--测试点4：创建列存范围分区表，表中存在数据，数据不唯一且有空值
drop table if exists column_part_tab19;
create table column_part_tab19(id int,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));
insert into column_part_tab19 values(null,null),('',null),(null,'');
insert into column_part_tab19 values(generate_series(1,1000),'b_'||generate_series(1,1000));

--创建唯一索引,指定索引分区的名称，合理报错
create unique index column_index19 on column_part_tab19 using btree(id) local (partition idx_p1,partition idx_p2,partition idx_p3,partition idx_p4,partition idx_p5);

--删除表
drop table column_part_tab19 cascade;


--测试点5：创建列存范围分区表，表中不存在数据，添加唯一索引，插入数据
drop table if exists column_part_tab19;
create table column_part_tab19(id int,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));

--创建唯一索引
create unique index column_index19 on column_part_tab19 using btree(id) local;

--插入正常数据
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--再次插入已存在的数据，合理报错
insert into column_part_tab19 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--查看数据
select count(*) from column_part_tab19 where id=1;

--删除表
drop table column_part_tab19 cascade;