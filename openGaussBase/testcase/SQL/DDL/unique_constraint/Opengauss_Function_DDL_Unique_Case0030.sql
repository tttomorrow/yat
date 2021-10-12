-- @testpoint: 插入相同数据后再对其中一列创建唯一约束，合理报错
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint030;
create table test_unique_constraint030(
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
--创建复合唯一约束
alter table test_unique_constraint030 add constraint personid_yewrtwytr unique (netypeid,counterid);
--bool类型列插入不同数据，成功
insert into test_unique_constraint030 values(1,1,1,26,56,8,290,0,false,10,'1010',7779,2630,1);
insert into test_unique_constraint030 values(2,2,-25,26,56,8,290,0,true,10,'1010',7779,2630,1);
--bool类型列再次插入true,成功
insert into test_unique_constraint030 values(3,3,'32767',26,56,8,290,0,true,10,'1010',7779,2630,1);
--custom创建唯一约束，合理报错
alter table test_unique_constraint030 add constraint custom_constr unique (custom);
--删表
drop table test_unique_constraint030;
