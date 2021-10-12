-- @testpoint: 创建分区表

drop table if exists partition_range01;
create table partition_range01(
ID   integer,
name   char(10),
CLASS   varchar(20),
COURSE  char(10),
SCORE    integer
)partition by range(SCORE)
 (
partition part01 values less than (0),
partition part02 values less than (60),
partition part03 values less than (80),
partition part04 values less than (90),
partition part05 values less than (maxvalue)
 );
insert into partition_range01 values(1,'小明','三班','英语',86),(2,'小红','三班','英语',86),(3,'小胖','三班','英语',86);
insert into partition_range01 values(1,'小明','2班','语文',96),(2,'小红','2班','语文',86),(3,'小胖','2班','语文',86);
insert into partition_range01 values(4,'小明','1班','shuxue',100),(2,'小红','2班','shuxue',86),(3,'小胖','2班','语文',86);
select * from partition_range01;
drop table if exists partition_range01;
