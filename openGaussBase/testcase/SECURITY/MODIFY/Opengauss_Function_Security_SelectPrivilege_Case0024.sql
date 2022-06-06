-- @testpoint: 三权分立关闭时验证用户对于私有模式下的表没有select权限,赋予select权限之后可以查询表,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:成功
drop user if exists u_selectprivilege_0024;
drop user if exists u_selectprivilege_0024_1;
create user u_selectprivilege_0024   password 'test@123';
create user u_selectprivilege_0024_1  password 'test@123';

--step3: 切换用户1创建表并向表中插入数据,将schema访问权限赋予用户2; expect:成功
set role u_selectprivilege_0024 password 'test@123';
select current_user;
create table u_selectprivilege_0024.t_selectprivilege_0024(id int,name varchar(100));
insert into u_selectprivilege_0024.t_selectprivilege_0024 values(1,'beijing'),(2,'shanghai');
grant usage on schema u_selectprivilege_0024 to u_selectprivilege_0024_1;

--step4: 切换用户2查询表; expect:合理报错
reset role;
set role u_selectprivilege_0024_1 password 'test@123';
select current_user;
select * from  u_selectprivilege_0024.t_selectprivilege_0024;

--step5: 切换用户1授权; expect:成功
reset role;
set role u_selectprivilege_0024 password 'test@123';
select current_user;
grant select on table u_selectprivilege_0024.t_selectprivilege_0024 to u_selectprivilege_0024_1;

--step6: 切换用户2查询表; expect:查询结果与插入数据一致
reset role;
set role u_selectprivilege_0024_1 password 'test@123';
select current_user;
select * from  u_selectprivilege_0024.t_selectprivilege_0024;

--step7: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step8: 清理环境; expect:环境清理成功
drop table u_selectprivilege_0024.t_selectprivilege_0024;
drop user u_selectprivilege_0024 cascade;
drop user u_selectprivilege_0024_1 cascade;