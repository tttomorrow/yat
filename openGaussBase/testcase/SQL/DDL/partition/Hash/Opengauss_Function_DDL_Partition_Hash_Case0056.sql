-- @testpoint: Hash分区表结合LIKE INCLUDING  CONSTRAINTS参数 插入0和负数时合理报错

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;
create table partition_hash_tab
(id                        number(7) check(id>0),
 use_filename               varchar2(20) ,
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入正确数据 expect：成功
insert into partition_hash_tab values(10,'张三','数学','老师');

--step3：插入数据id=0 expect：check约束导致合理报错
insert into partition_hash_tab values(0,'张三','数学','老师');

--step4：插入数据id为负数 expect：check约束导致合理报错
insert into partition_hash_tab values(-10,'张三','数学','老师');

--step5：查看数据 expect：只有step2中插入的数值
select * from partition_hash_tab;

--step6：使用like参数建表 expect：成功
create table partition_hash_tab_like (like  partition_hash_tab including constraints);

--step7：插入正确数据 expect：成功
insert into partition_hash_tab_like values(3,'李四','数学系','学生');

--step8：插入数据id为负数 expect：check约束导致合理报错
insert into partition_hash_tab_like values(-4,'李四','数学系','学生');

--step9：查看数据 expect：只有step7中插入的数值
select * from partition_hash_tab_like;

--step10：清理环境 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;