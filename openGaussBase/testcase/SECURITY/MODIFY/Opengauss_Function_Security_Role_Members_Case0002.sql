-- @testpoint: 三权分立关闭时验证用户不能相互建立角色成员关系,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:用户创建成功
create user u_sec_role_member_auditadmin_002  auditadmin   password 'test@123';
create user u_sec_role_member_createrole_002  createrole   password 'test@123';

--step3: grant 用户2 to 用户1; expect:成功
grant u_sec_role_member_createrole_002 to u_sec_role_member_auditadmin_002;

--step4: grant 用户1 to 用户2; expect:合理报错
grant u_sec_role_member_auditadmin_002 to u_sec_role_member_createrole_002;

--step5: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_auditadmin_002','u_sec_role_member_createrole_002') order by 1,2;

--step6: 清理环境; expect:成功
drop user u_sec_role_member_auditadmin_002;
drop user u_sec_role_member_createrole_002;
