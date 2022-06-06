-- @testpoint: hash分区表上以delete方式创建触发器

--step1：创建hash分区表、触发表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);
drop table if exists partition_hash_des_tab;
create table partition_hash_des_tab(p_id int);

--step2：插入数据 expect：成功
begin
  for i in 1..20 loop
    insert into partition_hash_tab values(i);
  end loop;
end;
/

--step3：创建触发器函数 expect：成功
create or replace function delete_func() returns trigger as
           $$
           declare
           begin
                   INSERT INTO partition_hash_des_tab VALUES(1);
                   RETURN null;
           end
           $$ language plpgsql;
/

--step4：创建delete触发器 expect：成功
create trigger delete_trigger
           after delete on partition_hash_tab
           execute procedure delete_func();
/

--step5：delete数据 expect：成功
delete partition_hash_tab where p_id=1;

--step6：查看触发器是否生效 expect：成功
select * from partition_hash_des_tab;

--step7：清理环境 expect：成功
drop trigger delete_trigger on partition_hash_tab;
drop table if exists partition_hash_tab cascade;
drop table if exists partition_hash_des_tab cascade;
drop function if exists delete_func();