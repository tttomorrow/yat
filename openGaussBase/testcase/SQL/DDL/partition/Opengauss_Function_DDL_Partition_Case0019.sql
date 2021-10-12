-- @testpoint: 范围分区表，DDL+统计信息

drop table if exists partition_range00026;
create table partition_range00026(
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
field18  varchar(1024)
)partition by range(field12)
  (
partition part01 values less than (TO_DATE('2008-07-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part02 values less than (TO_DATE('2008-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part03 values less than (TO_DATE('2008-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part04 values less than (maxvalue)
 );

  declare
i int:=0;
begin
  loop
    i:=i+1;
insert into partition_range00026  values(256,10000000,123.3212,123456.123,123456,'dnf','957',
'2012-11-11 00:00:00',interval '2' day,'2016-12-11 00:00:00','2011-12-11 00:00:00','true',null);
exit when i= 100;
  end loop;
  raise info'111';
end;
/
commit;

create index index_partition_range000260 on partition_range00026(field1,field15,field11) local;

alter table partition_range00026 add field19  raw(1027);
alter table partition_range00026 add field20  varchar(10);
alter table partition_range00026 add field21  varchar2(20);

alter table partition_range00026 modify (field20 varchar2(500));

alter table partition_range00026 drop column field20;


alter table partition_range00026 rename column field21 to field20;

create index index_partition_range000261 on partition_range00026(field1,field15,field18) local;
create index index_partition_range000262 on partition_range00026(field1) local;
create index index_partition_range000263 on partition_range00026(field7) local;
create index index_partition_range000264 on partition_range00026(field1,field6,field15) local;
create index index_partition_range000265 on partition_range00026(field12) local;
create index index_partition_range000266 on partition_range00026(field17) local;
create index index_partition_range000267 on partition_range00026(field18) local;
create index index_partition_range000268 on partition_range00026(field19) local;
create index index_partition_range000269 on partition_range00026(upper(field6)) local;


update partition_range00026 set field15 = '2018-12-17 12:48:33.216000';

alter table partition_range00026 add(aaa BINARY_INTEGER default 222 not null);

alter table partition_range00026 add(name VARCHAR(24) default 'dddddddddddd' not null);

delete from partition_range00026;
rollback;

truncate table partition_range00026;
drop table partition_range00026;






