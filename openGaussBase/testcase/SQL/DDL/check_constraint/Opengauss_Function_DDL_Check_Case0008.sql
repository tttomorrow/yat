-- @testpoint: 插入数据后对布尔类型列进行约束，已有数据违背check项，设置失败，合理报错
drop table if exists tb_test;
create table tb_test(
 NeTypeId int not null,CounterId int not null,GranulityPeriod smallint not null,Name nvarchar2(4) not null,
 Description nvarchar2(4000),Description_set nvarchar2(100),SOURCE_CLASS_ID bigint not null,SOURCE_ATTRIBUTE_ID bigint,
 CUSTOM BOOLEAN default true,TENANT_ID varchar(20) default null,Strings blob,UserId int,ActiveDstOffset number(5) not null,
 QueryFrequency int default 0 not null
);
alter table tb_test add constraint PersonID unique (NeTypeId,CounterId);
--bool类型插入不同数据
insert into tb_test values(1,1,1,26,56,8,290,0,false,10,'1010',7779,2630,1);
insert into tb_test values(2,2,-25,26,56,8,290,0,true,10,'1010',7779,2630,1);
--对bool类型插入大于0的约束成功
alter table tb_test add constraint CUSTOM_constr check (CUSTOM = true);
drop table tb_test cascade;