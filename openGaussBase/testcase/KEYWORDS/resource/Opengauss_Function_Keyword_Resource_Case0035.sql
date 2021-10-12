-- @testpoint: opengauss关键字resource(非保留)，设置角色使用的resource pool名称

--查看资源池信息
select * from pg_resource_pool;

--设置角色使用的resource pool名称
DROP ROLE if exists manager;
CREATE ROLE manager RESOURCE POOL 'default_pool' IDENTIFIED BY 'Bigdata@123';

--清理环境
DROP ROLE manager;
