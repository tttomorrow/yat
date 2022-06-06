-- @testpoint: 三权分立关闭时验证将用户加入到组之后（有with admin option选项），用户可以将组成员关系赋给其他用户

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:用户创建成功
create user u_sec_role_member_normaluser_001    password 'test@123';
create user u_sec_role_member_auditadmin_001  auditadmin   password 'test@123';
create user u_sec_role_member_createrole_001  createrole   password 'test@123';

--step3: 用户1和2之间建立成员关系之后，取消成员关系，并且查询系统表; expect:成功
grant all privileges on pg_catalog.pg_roles to u_sec_role_member_auditadmin_001;
grant u_sec_role_member_normaluser_001 to u_sec_role_member_auditadmin_001 with admin option;
set session authorization u_sec_role_member_auditadmin_001 password 'test@123';
grant u_sec_role_member_normaluser_001 to u_sec_role_member_createrole_001 with admin option;
select a.rolname as member,(select c.rolname from pg_roles c where c.oid = b.member) as rolname   from pg_roles a, pg_auth_members b  where a.oid = b.roleid and a.rolname in('u_sec_role_member_normaluser_001','u_sec_role_member_auditadmin_001','u_sec_role_member_createrole_001') order by 1,2;

--step4: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step5: 用户1创建表; expect:成功
set session authorization u_sec_role_member_normaluser_001 password 'test@123';
create  table u_sec_role_member_normaluser_001.t_secrole_member_001(id int primary key,name varchar(100));

--step6: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step7: 用户3对用户1创建的对象有权限; expect:成功
set session authorization u_sec_role_member_createrole_001 password 'test@123';
insert into  u_sec_role_member_normaluser_001.t_secrole_member_001 values(1,'beijing'),(2,'xian');
select * from  u_sec_role_member_normaluser_001.t_secrole_member_001;
update  u_sec_role_member_normaluser_001.t_secrole_member_001 set name='shanxi' where id=1;
delete from   u_sec_role_member_normaluser_001.t_secrole_member_001  where id=1;
truncate table   u_sec_role_member_normaluser_001.t_secrole_member_001;

--step8: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step9: 清理环境; expect:成功
revoke all privileges on pg_catalog.pg_roles from u_sec_role_member_auditadmin_001;
drop table u_sec_role_member_normaluser_001.t_secrole_member_001;
drop user u_sec_role_member_auditadmin_001;
drop user u_sec_role_member_createrole_001;
drop user u_sec_role_member_normaluser_001;