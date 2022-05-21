-- @testpoint: 三权分立关闭时验证非超级用户对其他用户在public模式下创建的表没有select权限，赋权之后可以查询,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:成功
drop user if exists u_selectprivilege_0031;
drop user if exists u_selectprivilege_0031_1;
create user u_selectprivilege_0031 auditadmin  password 'test@123';
create user u_selectprivilege_0031_1 password 'test@123';

--step3: 切换用户1创建表并插入数据并将schema权限赋予用户2; expect:成功
set role u_selectprivilege_0031 password 'test@123';
select current_user;
create table u_selectprivilege_0031.t_selectprivilege_0031(id int,name varchar(100));
insert into u_selectprivilege_0031.t_selectprivilege_0031 values(1,'beijing'),(2,'shanghai');
grant usage on schema u_selectprivilege_0031 to u_selectprivilege_0031_1;

--step4: 切换用户2查询表; expect:合理报错
reset role;
set role u_selectprivilege_0031_1 password 'test@123';
select current_user;
select * from  u_selectprivilege_0031.t_selectprivilege_0031;

--step5: 切换用户1授权; expect:成功
reset role;
set role u_selectprivilege_0031 password 'test@123';
select current_user;
grant select on table u_selectprivilege_0031.t_selectprivilege_0031 to u_selectprivilege_0031_1;


--step6: 切换用户2查询表; expect:成功
reset role;
set role u_selectprivilege_0031_1 password 'test@123';
select current_user;
select * from  u_selectprivilege_0031.t_selectprivilege_0031;

--step7: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step8: 清理环境; expect:环境清理成功
drop table u_selectprivilege_0031.t_selectprivilege_0031;
drop user u_selectprivilege_0031 cascade;
drop user u_selectprivilege_0031_1 cascade;