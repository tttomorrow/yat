-- @testpoint: opengauss关键字resource(非保留)，设置角色使用的resource pool名称

--step1：查看资源池信息; expect:成功
select * from pg_resource_pool;

--step2：设置角色使用的resource pool名称; expect:成功
DROP ROLE if exists manager;
CREATE ROLE manager RESOURCE POOL 'default_pool' IDENTIFIED BY 'Bigdata@123';

--step4：清理环境; expect:成功
DROP ROLE manager;
