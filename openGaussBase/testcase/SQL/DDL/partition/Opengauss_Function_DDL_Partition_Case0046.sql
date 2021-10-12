-- @testpoint: 范围分区全部数据类型，测试局部索引空表的analyze功能

drop table if exists partition_range030;
create table partition_range030(
field1   integer,
field2   bigint,
field3   real,
field4   decimal(10,2),
field5   number(6),
field6   char(10),
field7   varchar(10),
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
)partition by range(field12)
  (
      partition part01 values less than (TO_DATE('2008-07-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
      partition part02 values less than (TO_DATE('2008-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
      partition part03 values less than (TO_DATE('2008-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part04 values less than (maxvalue)
 );
create index index_partition_range030  on partition_range030(field1,field7,field11,field12,field17) local;---多列局部索引
create index index_partition_range0301 on partition_range030(field19,field18,field11) local;---多列局部索引
create index index_partition_range0302 on partition_range030(field5) local;

analyze verbose  partition_range030 ;
drop table if exists partition_range030;