-- @testpoint: List分区表以隔离级别为READ COMMITTED，访问模式为READ WRITE启动事务,合理报错

--step01:创建list分区表;expect:成功
drop table if exists t_partition_list_0051;
create table t_partition_list_0051
(id                        NUMBER(7),
 use_filename               VARCHAR2(20) ,
 filename                   VARCHAR2(255) ,
 text                       VARCHAR2(2000))
partition by  list(id)
(partition p1 values(1),
 partition p2 values(2),
 partition p3 values(3),
 partition p4 values(4)
 );

--step02:以隔离级别为READ COMMITTED，访问模式为READ WRITE启动事务插入数据;expect:合理报错
begin work isolation level read committed read write;
insert into t_partition_list_0051 values (1);
insert into t_partition_list_0051 values (2);
insert into t_partition_list_0051 values (3);
insert into t_partition_list_0051 values (4);
END;
/
--step03: 查看数据;expect:成功
select * from t_partition_list_0051 order by id asc;

--step04: 清理数据;expect:成功
drop table if exists t_partition_list_0051 cascade;
