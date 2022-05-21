-- @testpoint: 三权分立关闭时验证两个用户有继承关系用户不能循环建立角色成员关系,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableseparationofduty;

--step2: 创建普通用户; expect:用户创建成功
create user u_sec_role_member_normaluser_004_01 with noinherit   password 'test@123';
create user u_sec_role_member_normaluser_004_02  with inherit   password 'test@123';

--step3: 切换用户1,将schema权限授权给用户2; expect:成功
set role u_sec_role_member_normaluser_004_01 password 'test@123';
select current_user;
grant create on schema u_sec_role_member_normaluser_004_01 to u_sec_role_member_normaluser_004_02;

--step4: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step5: 切换用户2创建表; expect:创建表失败
grant all privileges on pg_catalog.pg_roles to u_sec_role_member_normaluser_004_02;
set role u_sec_role_member_normaluser_004_02 password 'test@123';
select current_user;
create table u_sec_role_member_normaluser_004_01.t_sec_role_member_004_01(id int primary key,name varchar(100));

--step6: 查看系统成员; expect:查询成功
select a.rolname   from pg_roles a where a.oid=(select b.relowner from pg_class b where b.relname='t_sec_role_member_004_01');

--step7: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step8: 切换用户1, grant 用户1给用户2 ; expect:授权失败
set role u_sec_role_member_normaluser_004_01 password 'test@123';
select current_user;
grant u_sec_role_member_normaluser_004_01 to u_sec_role_member_normaluser_004_02;

--step9: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step10: 切换用户2创建表; expect:创建表失败
set role u_sec_role_member_normaluser_004_02 password 'test@123';
select current_user;
create table u_sec_role_member_normaluser_004_01.t_sec_role_member_004_02(id int primary key,name varchar(100));

--step11: 查看系统成员; expect:查询成功
select a.rolname   from pg_roles a where a.oid=(select b.relowner from pg_class b where b.relname='t_sec_role_member_004_02');

--step12: 重置当前用户; expect:重置成功
reset role;
select  current_user;

--step14: 清理环境; expect:成功
revoke all privileges on pg_catalog.pg_roles from u_sec_role_member_normaluser_004_02;
drop user u_sec_role_member_normaluser_004_01 cascade;
drop user u_sec_role_member_normaluser_004_02 cascade;