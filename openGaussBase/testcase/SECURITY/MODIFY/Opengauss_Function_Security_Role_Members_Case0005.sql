-- @testpoint: 三权分立关闭时验证可以将用户多次加入同一个组中，但只要一次revoke就可以从组中去除成员

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:用户创建成功
create user u_sec_role_member_sysadmin_005 sysadmin   password 'test@123';
create user u_sec_role_member_auditadmin_005  auditadmin   password 'test@123';
create user u_sec_role_member_createrole_005  createrole   password 'test@123';

--step3: grant 用户1给用户2 ; expect:成功
grant u_sec_role_member_sysadmin_005 to u_sec_role_member_auditadmin_005 with admin option;

--step4: 切换用户1, grant 用户1给用户2 ; expect:授权成功
set session authorization u_sec_role_member_sysadmin_005 password 'test@123';
select session_user,current_user;
grant u_sec_role_member_sysadmin_005 to u_sec_role_member_auditadmin_005 with admin option;

--step5: 查看系统成员; expect:查询成功
select a.rolname   from pg_roles a where a.oid=(select b.relowner from pg_class b where b.relname='t_sec_role_member_004_02');

--step6: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step7:回收权限 ; expect:成功
revoke u_sec_role_member_sysadmin_005 from u_sec_role_member_auditadmin_005;

--step8: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_sysadmin_005','u_sec_role_member_auditadmin_005','u_sec_role_member_createrole_005');

--step9: 清理环境; expect:成功
drop user u_sec_role_member_sysadmin_005 cascade;
drop  user u_sec_role_member_auditadmin_005 cascade;
drop  user u_sec_role_member_createrole_005 cascade;