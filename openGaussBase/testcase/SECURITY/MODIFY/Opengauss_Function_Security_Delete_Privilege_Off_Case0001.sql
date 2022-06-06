-- @testpoint: 三权分立关闭时验证超级用户对其他用户(普通用户)创建的表有DELETE权限

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建普通用户; expect:用户创建成功
drop user if exists u_delete_privilege_off_0001;
create user u_delete_privilege_off_0001  password 'test@123';

--step3: 切换用户; expect:用户切换成功
set session authorization u_delete_privilege_off_0001 password 'test@123';
select session_user,current_user;

--step4: 创建表; expect:表创建成功
drop table if exists t_delete_privilege_off_0001;
create table u_delete_privilege_off_0001.t_delete_privilege_off_0001(id int,name varchar(100));

--step5: 向表中插入数据; expect:数据插入成功
insert into u_delete_privilege_off_0001.t_delete_privilege_off_0001 values(1,'beijing');

--step6: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step7: 管理员权限delete表记录; expect:表记录清除成功
delete from u_delete_privilege_off_0001.t_delete_privilege_off_0001;

--step8: 查询清空的表; expect:查询结果为空
select *  from u_delete_privilege_off_0001.t_delete_privilege_off_0001;

--step9: 清理环境; expect:环境清理成功
drop table u_delete_privilege_off_0001.t_delete_privilege_off_0001;
drop user u_delete_privilege_off_0001;