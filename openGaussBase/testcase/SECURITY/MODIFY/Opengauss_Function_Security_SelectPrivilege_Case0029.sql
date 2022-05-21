-- @testpoint: 三权分立关闭时验证用户对于public模式下的全局临时表没有select权限,赋予select权限之后可以查询表,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:成功
drop user if exists u_selectprivilege_0029;
drop user if exists u_selectprivilege_0029_1;
create user u_selectprivilege_0029 createrole  password 'test@123';
create user u_selectprivilege_0029_1 password 'test@123';

--step3: 切换createrole用户创建全局临时表并插入数据; expect:成功
set role u_selectprivilege_0029 password 'test@123';
select current_user;
create temp table t_selectprivilege_0029(id int,name varchar(100));
insert into t_selectprivilege_0029 values(1,'beijing'),(2,'shanghai');

--step4: 切换用户2查询表; expect:合理报错
reset role;
set role u_selectprivilege_0029_1  password 'test@123';
select current_user;
select * from  t_selectprivilege_0029;

--step5: 切换用户1授权; expect:成功
reset role;
set role u_selectprivilege_0029  password 'test@123';
select current_user;
grant select on table t_selectprivilege_0029 to u_selectprivilege_0029_1;

--step6: 切换用户2查询表; expect:成功
reset role;
set role u_selectprivilege_0029_1  password 'test@123';
select current_user;
select * from  t_selectprivilege_0029;

--step7: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step8: 清理环境; expect:环境清理成功
drop table t_selectprivilege_0029;
drop user u_selectprivilege_0029;
drop user u_selectprivilege_0029_1;