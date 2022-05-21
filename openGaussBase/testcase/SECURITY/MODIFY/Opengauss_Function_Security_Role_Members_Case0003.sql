-- @testpoint: 三权分立关闭时验证多个用户不能循环建立角色成员关系,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:用户创建成功
create user u_sec_role_member_auditadmin_003  auditadmin   password 'test@123';
create user u_sec_role_member_createrole_003  createrole   password 'test@123';
create user u_sec_role_member_normaluser_003  createdb   password 'test@123';
create user u_sec_role_member_normaluser1_003   password 'test@123';

--step3: 赋权限; expect:成功
grant all privileges on pg_catalog.pg_roles to u_sec_role_member_createrole_003;

--step4: 切换用户2,grant 用户1to用户3; expect:成功
set session authorization u_sec_role_member_createrole_003 password 'test@123';
select session_user,current_user;
grant u_sec_role_member_auditadmin_003 to u_sec_role_member_normaluser_003;

--step5: grant 用户3to用户4; expect:成功
grant u_sec_role_member_normaluser_003 to u_sec_role_member_normaluser1_003;

--step6: grant 用户4to用户1; expect:合理报错
grant u_sec_role_member_normaluser1_003 to u_sec_role_member_auditadmin_003;

--step7: 查看系统成员; expect:查询成功
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_auditadmin_003','u_sec_role_member_createrole_003','u_sec_role_member_normaluser_003','u_sec_role_member_normaluser1_003') order by 1,2;

--step8: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step9: 清理环境; expect:成功
drop user u_sec_role_member_auditadmin_003 cascade;
drop user u_sec_role_member_createrole_003 cascade;
drop user u_sec_role_member_normaluser_003 cascade;
drop user u_sec_role_member_normaluser1_003 cascade;