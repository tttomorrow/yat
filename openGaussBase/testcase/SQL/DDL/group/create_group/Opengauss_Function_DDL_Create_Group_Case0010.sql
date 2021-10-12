--  @testpoint:创建用户组,指定RESOURCE POOL
--通过系统表pg_resource_pool，查询resource pool名称
select respool_name from pg_resource_pool;
--创建用户组，指定RESOURCE POOL
drop group if exists test_group9;
create group test_group9 with RESOURCE POOL 'default_pool' PASSWORD 'Xiaxia@123';
--查看用户所能够使用的resource pool
select rolname,rolrespool from pg_authid where rolname = 'test_group9';
--修改用户的resource pool不属于系统表pg_resource_pool，合理报错
alter group test_group9 with RESOURCE POOL 'default_pools';
--删除group
drop group test_group9;