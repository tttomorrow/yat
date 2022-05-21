-- @testpoint: 三权分立关闭时验证超级用户对其他用户(普通用户)创建的分区表有DELETE权限

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建普通用户; expect:用户创建成功
create user u_delete_privilege_off_0002  createrole password 'test@123';

--step3: 切换用户; expect:用户切换成功
set session authorization u_delete_privilege_off_0002 password 'test@123';
select session_user,current_user;

--step4: 创建分区表; expect:创建成功
create table u_delete_privilege_off_0002.t_delete_privilege_off_0002(id int,name varchar(100))
    partition by range(id)
    (
    partition p1 values less than(10),
    partition p2 values less than(20),
    partition p3 values less than(30),
    partition pmax values less than(maxvalue)
    );
--step5: 向表中插入数据; expect:数据插入成功
insert into u_delete_privilege_off_0002.t_delete_privilege_off_0002 values(1,'beijing'),(11,'shanghai');

--step6: 重置当前用户; expect:重置成功
reset session authorization;
select session_user,current_user;

--step7: 管理员权限delete分区表记录; expect:分区表记录清除成功
delete from u_delete_privilege_off_0002.t_delete_privilege_off_0002 where id=1;

--step8: 查询清空的表; expect:查询结果与预期结果一致
select *  from u_delete_privilege_off_0002.t_delete_privilege_off_0002;

--step9: 清理环境; expect:环境清理成功
drop table u_delete_privilege_off_0002.t_delete_privilege_off_0002;
drop user u_delete_privilege_off_0002;