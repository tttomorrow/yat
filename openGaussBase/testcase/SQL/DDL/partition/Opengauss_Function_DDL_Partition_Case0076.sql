-- @testpoint: 建立分区表并插入数据，然后对该分区表中的一个分区循环做split和merge一段时间后，执行vacuum freeze pg_partition

--step1:创建分区表; expect:成功
drop table if exists t_partition_0076;
create table t_partition_0076(ca_address_sk integer not null,ca_address_id character(16))
partition by range (ca_address_sk)
(partition p1 values less than(10000),
 partition p2 values less than(20000),
 partition p3 values less than(30000),
 partition p4 values less than(40000),
 partition p5 values less than(maxvalue))
enable row movement;

--step2:创建存储过程，插入数据; expect:成功
create or replace procedure p_partition_0076_01()
as
begin
    for i in 0..200000 loop
        insert into t_partition_0076 values(i,'a_'|| i);
    end loop;
end;
/
call p_partition_0076_01();

--step3:创建存储过程,对分区循环做split和merge; expect:成功
create or replace procedure p_partition_0076_02()
as
begin
    for i in 0..20 loop
        alter table t_partition_0076 split partition p5 at (50000) into(partition p6,partition p7);
        alter table t_partition_0076 merge partitions p6,p7 into partition p5;
    end loop;
end;
/
call p_partition_0076_02();

--step4:执行vacuum freeze; expect:成功
vacuum freeze t_partition_0076 partition(p5);

--step5:清理环境; expect:成功
drop table t_partition_0076 cascade;
drop procedure p_partition_0076_01;
drop procedure p_partition_0076_02;
