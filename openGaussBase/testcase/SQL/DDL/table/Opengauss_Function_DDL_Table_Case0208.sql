-- @testpoint: alter table partition_clauses  枚举分区表插入'',合理报错
drop table if exists alter_table_tb004;
create table alter_table_tb004
(c1 int PRIMARY KEY,
c2 bigint,
c3 varchar(20)
) PARTITION BY RANGE (c1) (PARTITION p1 VALUES less than (25), PARTITION p2 VALUES less than (50),PARTITION p3 VALUES less than (75),PARTITION p4 VALUES less than (100));
insert into alter_table_tb004 values('11',null,'sss');
insert into alter_table_tb004 values('21','','ss');
insert into alter_table_tb004 values('31',66,'');
insert into alter_table_tb004 values('41',66,null);
insert into alter_table_tb004 values('51',66,'null');
insert into alter_table_tb004 values('61',66,'cc');

--error
alter table alter_table_tb004  ADD PARTITION p5 values less than(' ') ;

insert into alter_table_tb004 values('21','','bb');
insert into alter_table_tb004 values('21','','ss');
insert into alter_table_tb004 values('81','','');

--error
alter table alter_table_tb004  drop  PARTITION p5 ;
alter table alter_table_tb004 modify c1 varchar(20) DEFAULT 'we';

SELECT COUNT(*) FROM alter_table_tb004 PARTITION ;
SELECT COUNT(*) FROM alter_table_tb004 PARTITION (p3);
drop table if exists alter_table_tb004;