-- @testpoint: 参数session_replication_role保持默认值origin，验证功能,向子表外键插入/更新入主表不存在的值，合理报错
--查看默认值
show session_replication_role;
--建主表
drop table if exists test01 cascade;
create table test01 (id int primary key, col1 varchar(10));
--建子表
drop table if exists test02 cascade;
create table test02 (id int primary key, t1_id int);
--创建约束
alter table test02 add constraint test02_t1_id_fkey foreign key (t1_id) references test01 (id) on delete cascade on update restrict ;
--向主表插入值
insert into test01 values (1,'a');
--向子表插入值
insert into test02 values (1,1);
--向子表外键插入主表不存在的值，报错
insert into test02 values (2,2);
--子表外键更新主表不存在的值，报错
update test02 set t1_id = 2 where t1_id = 1;
--主表主键更新，报错
update test01 set id = 2 where id = 1;
--主表主键删除，成功,子表关联键一同删除
delete from test01 where id = 1;
select * from test02;
--清理环境
drop table if exists test01 cascade;
drop table if exists test02 cascade;