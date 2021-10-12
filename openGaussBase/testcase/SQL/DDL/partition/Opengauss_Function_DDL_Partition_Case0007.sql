-- @testpoint: 范围分区表，分区键为数值(timestamp)，测试DBMS高级包收集统计信息功能

drop table if exists partition_range00015;
create table partition_range00015(
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
field14 INTERVAL DAY(7) TO SECOND(4),
field15 timestamp with time zone,
field16 timestamp,
field17 boolean,
field18  varchar(1024),
field19  raw(1027)
)partition by range(field13)
  (
partition part01 values less than (TO_DATE('2003-07-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part02 values less than (TO_DATE('2005-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part03 values less than (TO_DATE('2008-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part04 values less than (TO_DATE('2009-07-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part05 values less than (TO_DATE('2010-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part06 values less than (TO_DATE('2012-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part07 values less than (TO_DATE('2014-06-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part08 values less than (TO_DATE('2015-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part09 values less than (TO_DATE('2016-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part10 values less than (TO_DATE('2017-05-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part11 values less than (TO_DATE('2018-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
partition part12 values less than (maxvalue)
 );
 declare
i int:=0;
begin
  loop
    i:=i+1;
'2012-11-11 00:00:00',interval '2' day,'2016-12-11 00:00:00','2011-12-11 00:00:00','true',null,null);
exit when i= 1000;
  end loop;
  raise info'111';
end;
/
drop table partition_range00015;