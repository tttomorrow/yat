-- @testpoint: 设置参数参数session_replication_role为replica，验证功能
--查看默认值
show session_replication_role;
--设置
set session_replication_role to replica;
--查询
show session_replication_role ;
--建主表
drop table if exists test01 cascade;
create table test01 (id int primary key, col1 varchar(10));
--建子表
drop table if exists test02 cascade;
create table test02 (id int primary key, t1_id int);
--建外键
alter table test02 add constraint test02_t1_id_fkey foreign key (t1_id) references test01 (id) on delete cascade on update restrict ;
-- 向主表插入值
insert into test01 values (1,'a');
-- 向子表插入值
insert into test02 values (1,1);
-- 向子表外键插入主表不存在的值，成功
insert into test02 values (2,2);
-- 子表外键更新主表不存在的值，成功
update test02 set t1_id = 11 where t1_id = 1;
-- 主表主键更新，成功
 update test01 set id = 3 where id = 1;
 update test01 set id = 2 where id = 3;
-- 主表主键删除，成功,子表关联键不会删除（所有操作均已成功，说明外键已失效）
delete from test01 where id = 2;
select * from test02;
--查看外键trigger的状态(触发器在“origin”和“local”模式下触发)
select distinct tgenabled from pg_catalog.pg_trigger where tgconstraint = (select oid from pg_catalog.pg_constraint pcon where conname = 'test02_t1_id_fkey');
--清理环境
drop table if exists test01 cascade;
drop table if exists test02 cascade;
--恢复默认值
set session_replication_role to origin;