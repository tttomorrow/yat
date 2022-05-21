-- @testpoint: Hash分区表结合关键字USING INDEX TABLESPACE

--step1：创建表空间 expect：成功
drop tablespace if exists index_tablespace;
create tablespace index_tablespace relative location 'tablespace/tablespace_1';

--step2：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0070_01;
create table t_partition_hash_0070_01(
id int primary key using index tablespace  index_tablespace ,
name varchar(100))
partition by hash(id)
(partition p1,
 partition p2);

--step3：插入数据 expect：成功插入2000条数据
begin
  for i in 1..2000 loop
    insert into t_partition_hash_0070_01 values(i);
  end loop;
end;
/

--step4：验证表空间的索引 expect：表空间中存在索引
select relname from pg_class t1 where relkind='i' and reltablespace=(
    select oid from pg_tablespace where spcname ='index_tablespace');

--step5：清理环境 expect：成功
drop table if exists t_partition_hash_0070_01;
drop tablespace if exists index_tablespace;