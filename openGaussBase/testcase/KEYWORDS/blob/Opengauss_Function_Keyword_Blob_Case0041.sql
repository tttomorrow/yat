-- @testpoint: 插入非法16进制字符串合理报错
DROP TABLE IF EXISTS t_blob;
create table t_blob(
    NeTypeId int not null,
    CounterId int not null,
    GranulityPeriod smallint not null,
    Name nvarchar2(4) not null,
    Description nvarchar2(4000),
 Description_set nvarchar2(100),
    SOURCE_CLASS_ID bigint not null,
 SOURCE_ATTRIBUTE_ID bigint,
 CUSTOM BOOLEAN default true,
 TENANT_ID varchar(20) default null,
 Strings blob,
    UserId int,
    ActiveDstOffset number(5) not null,
    QueryFrequency int default 0 not null
);
INSERT INTO t_blob VALUES(1,1,1,26,56,8,290,0,true,10,'2XFA278',7779,2630,1);
DROP TABLE IF EXISTS t_blob;