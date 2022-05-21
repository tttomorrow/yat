-- @testpoint: Hash分区表结合（foreign key）on update cascade on delete cascade

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab1;
create table if not exists partition_hash_tab1
(id         number(7) primary key,
name        varchar2(20))
partition by hash(id)
(partition p1,
 partition p2);
drop table if exists partition_hash_tab2;
create table if not exists partition_hash_tab2
(id         number(7) primary key,
name        varchar2(20))
partition by hash(id)
(partition p1,
 partition p2);

--step2：使用alter table建立外键 expect：成功
alter table partition_hash_tab2 add constraint fk_partition_hash_tab2_id
foreign key (id) references partition_hash_tab1(id)
on update cascade on delete cascade;

--step3：插入数据 expect：成功
insert into partition_hash_tab1 values(1,'张三');
insert into partition_hash_tab1 values(2,'李四');
insert into partition_hash_tab2 values(1,'张三');
insert into partition_hash_tab2 values(2,'李四');

--step4：查询数据 expect：成功
select * from partition_hash_tab1;
select * from partition_hash_tab2;

--step5：清理环境 expect：成功
drop table if exists partition_hash_tab2;
drop table if exists partition_hash_tab1;