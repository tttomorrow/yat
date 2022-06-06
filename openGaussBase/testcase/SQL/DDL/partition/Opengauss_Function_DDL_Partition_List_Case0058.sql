-- @testpoint: List分区表结合列约束（default）默认值和数据类型不匹配,合理报错

--step01:创建list分区表，default默认值与数据类型不匹配;expect:合理报错
drop table if exists t_partition_list_0058;
create table  t_partition_list_0058
(id               number(7)  ,
age           int  default 'aaa',
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by list(id)
(partition p1 values(1),
 partition p2 values(2));

