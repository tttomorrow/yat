-- @testpoint: list分区表，不支持的功能切割分区，合理报错

--创建list分区表
drop table if exists partition_list_tab;
create table partition_list_tab(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));


--切割分区,合理报错
alter table partition_list_tab split partition p2 INTO(partition q1 start(15) end(25) every(5));

--清理环境
drop table partition_list_tab;