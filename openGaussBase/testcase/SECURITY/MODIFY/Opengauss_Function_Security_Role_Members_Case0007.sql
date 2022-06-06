-- @testpoint: 三权分立关闭时验证用户被删除之后，组关系消失

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:用户创建成功
create user u_sec_role_member_sysadmin_007 sysadmin   password 'test@123';
create user u_sec_role_member_auditadmin_007  auditadmin   password 'test@123';
create user u_sec_role_member_createrole_007  createrole   password 'test@123';

--step3: 切换用户2，grant 用户1给用户2 ; expect:成功
set session authorization u_sec_role_member_sysadmin_007 password 'test@123';
select session_user,current_user;
grant u_sec_role_member_sysadmin_007 to u_sec_role_member_auditadmin_007 with admin option;

--step4: grant 用户1给用户3 ; expect:成功
grant u_sec_role_member_sysadmin_007 to u_sec_role_member_createrole_007 with admin option;

--step5: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_sysadmin_007','u_sec_role_member_auditadmin_007','u_sec_role_member_createrole_007') order by 1,2;

--step6: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step7:删除用户1 ; expect:成功
drop user u_sec_role_member_sysadmin_007;

--step8: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_sysadmin_007','u_sec_role_member_auditadmin_007','u_sec_role_member_createrole_007');

--step9: 清理环境; expect:成功
drop  user u_sec_role_member_auditadmin_007 cascade;
drop  user u_sec_role_member_createrole_007 cascade;