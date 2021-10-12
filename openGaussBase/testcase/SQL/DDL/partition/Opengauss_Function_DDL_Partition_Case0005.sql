-- @testpoint: 范围分区表，分区键为数值(Blob)，测试DBMS高级包收集统计信息功能,合理报错

drop table if exists partition_range00013;
create table partition_range00013(
field1   integer,
field2   bigint,
field3   real,
field4   decimal(10,2),
field5   number(38),
field6   char(10),
field7   varchar(2000),
field8   varchar2(20),
field9   CLOB,
field10  BLOB,
field11  varchar2(1024),
field12 date,
field13 timestamp,
field14 INTERVAL DAY(3) TO SECOND(4),
field15 timestamp with time zone,
field16 timestamp,
field17 boolean,
field18  varchar(1024),
field19  raw(1027)
)partition by range(field10)
  (
partition part01 values less than (lpad('345abc',50,'abc')),
partition part02 values less than (lpad('885abc',80,'abc')),
partition part14 values less than (maxvalue)
 );
