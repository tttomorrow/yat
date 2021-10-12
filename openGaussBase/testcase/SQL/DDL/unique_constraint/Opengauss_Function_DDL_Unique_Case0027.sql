-- @testpoint: 插入不同数据后,再创建唯一约束
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint027;
create table test_unique_constraint027(
netypeid int not null,
counterid int not null,
granulityperiod smallint not null,
name nvarchar2(4) not null,
description nvarchar2(4000),
description_set nvarchar2(100),
source_class_id bigint not null,
source_attribute_id bigint,
custom boolean default true,
tenant_id varchar(20) default null,
strings blob,
userid int,
activedstoffset number(5) not null,
queryfrequency int default 0 not null
);
--增加复合唯一约束
alter table test_unique_constraint027 add constraint person_id unique (netypeid,counterid);
--插入数据，custom列插入不同值，成功
insert into test_unique_constraint027 values(1,1,1,26,56,8,290,0,false,10,'1010',7779,2630,1);
insert into test_unique_constraint027 values(2,2,-25,26,56,8,290,0,true,10,'1010',7779,2630,1);
--custom列创建唯一约束，成功
alter table test_unique_constraint027 add constraint custom_constr unique (custom);
--查询约束信息
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint027') order by conname;
--删表
drop table test_unique_constraint027;
