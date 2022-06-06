-- @testpoint: 三权分立关闭时验证可以将用户多次从组中去除

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:用户创建成功
create user u_sec_role_member_sysadmin_006 sysadmin   password 'test@123';
create user u_sec_role_member_auditadmin_006  auditadmin   password 'test@123';

--step3: 切换用户2，grant 用户1给用户3 ; expect:成功
set session authorization u_sec_role_member_sysadmin_006 password 'test@123';
select session_user,current_user;
grant u_sec_role_member_sysadmin_006 to u_sec_role_member_auditadmin_006 with admin option;

--step4: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_sysadmin_006','u_sec_role_member_auditadmin_006','u_sec_role_member_createrole_006') order by 1,2;

--step5: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step6:回收权限 ; expect:成功
revoke u_sec_role_member_sysadmin_006 from u_sec_role_member_auditadmin_006;
revoke u_sec_role_member_sysadmin_006 from u_sec_role_member_auditadmin_006;

--step7: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_sysadmin_006','u_sec_role_member_auditadmin_006','u_sec_role_member_createrole_006');

--step8: 清理环境; expect:成功
drop user u_sec_role_member_sysadmin_006 cascade;
drop  user u_sec_role_member_auditadmin_006 cascade;