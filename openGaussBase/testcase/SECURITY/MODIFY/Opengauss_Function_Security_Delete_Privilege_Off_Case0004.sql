-- @testpoint: 三权分立关闭时验证超级用户可以delete用户私有模式下的局部临时表中的记录

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建普通用户; expect:用户创建成功
drop user if exists u_delete_privilege_off_0004 cascade;
create user u_delete_privilege_off_0004 createrole password 'test@123';

--step3: 切换用户; expect:用户切换成功
set session authorization u_delete_privilege_off_0004 password 'test@123';
select session_user,current_user;

--step4: 创建表; expect:创建成功
create local temp table t_delete_privilege_off_0004(id int,name varchar(100));

--step5: 向表中插入数据; expect:数据插入成功
insert into t_delete_privilege_off_0004 values(1,'beijing'),(11,'shanghai');

--step6: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step7: 管理员权限delete的记录; expect:表记录清除成功
delete from t_delete_privilege_off_0004 where id=1;

--step8: 查询delete后的表数据; expect:查询结果与预期结果一致
select * from t_delete_privilege_off_0004;

--step9: 清理环境; expect:环境清理成功
drop table t_delete_privilege_off_0004;
drop user u_delete_privilege_off_0004;