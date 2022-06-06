-- @testpoint: Hash分区表结合LIKE INCLUDING  DEFAULTS参数

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;
create table partition_hash_tab
(id                        number(7),
 use_filename               varchar2(20) ,
 filename                   varchar2(255) default 'test01',
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into partition_hash_tab(id,use_filename,text ) values(1,'张三','老师');
insert into partition_hash_tab(id,use_filename,text ) values(2,'张三','老师');

--step3：使用like参数建表 expect：成功
create table partition_hash_tab_like (like  partition_hash_tab including defaults);

--step4：插入数据 expect：成功
insert into partition_hash_tab_like(id,use_filename,text ) values(3,'李四','学生');
insert into partition_hash_tab_like(id,use_filename,text ) values(4,'李四','学生');

--step5：查询数据 expect：成功
select * from partition_hash_tab_like;

--step6：清理环境 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;