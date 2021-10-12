-- @testpoint: 修改视图所有者
--创建视图
create or replace view temp_view_026 as values(8,'worlcxcd');
--创建用户
drop user if exists user_view_026 cascade;
create user user_view_026 password 'test@123';
drop user if exists user1_view_026 cascade;
create user user1_view_026 password 'test@123';
--修改视图所有者
alter view if exists temp_view_026 owner to user_view_026;
--查询所有者
select viewname,viewowner from pg_views where viewname = 'temp_view_026';
--修改视图所有者，省略if exists
alter view temp_view_026 owner to user1_view_026;
--查询所有者
select viewname,viewowner from pg_views where viewname = 'temp_view_026';
--删除视图
drop view temp_view_026;
--删除用户
drop user user_view_026 cascade;
drop user user1_view_026 cascade;