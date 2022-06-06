-- @testpoint: Hash分区表结合LIKE INCLUDING  RELOPTIONS参数

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab
(id                         number(7) constraint partition_hash_tab_id_nn not null,
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
 )with(fillfactor=50);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'张三','数学','老师');

--step3：使用like参数建表 expect：成功
create table partition_hash_tab_like (like  partition_hash_tab including reloptions);

--step4：插入数据 expect：成功
insert into partition_hash_tab_like values(1,'李四','数学系','学生');

--step5：清理环境 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;