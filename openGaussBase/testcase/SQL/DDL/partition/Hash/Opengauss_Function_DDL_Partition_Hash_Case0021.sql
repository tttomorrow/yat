-- @testpoint: 创建普通hash分区表，结合存储过程

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar,p_age int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);

--step2：创建存储过程 expect：成功
create or replace procedure insert_partition_hash()
as
insert_str varchar;
begin
    for i in 0..5 loop
        insert_str = 'insert into partition_hash_tab values(10),(20),(30);';
        execute immediate insert_str;
    end loop;
end;
/

--step3：调用存储过程，向分区表中插入数据 expect：成功
call insert_partition_hash();

--step4：查看表中的数据 expect：成功
select * from partition_hash_tab;

--step4：清理环境 expect：成功
drop table partition_hash_tab;
drop procedure insert_partition_hash();