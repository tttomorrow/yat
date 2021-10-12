--- Case Type： Comment
--- Case Name： 在角色上添加注释

--创建角色
drop role if exists role_comment;
create role role_comment with password 'Xiaxia@123';

--给角色添加注释信息
comment on role role_comment is '测试角色注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_shdescription where objoid=(select oid from pg_roles where rolname='role_comment');

--清理环境
drop role role_comment;