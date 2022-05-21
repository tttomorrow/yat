-- @testpoint: 三权分立关闭时验证超级用户可以查询其他用户创建的表((超级用户为sysadmin权限，访问普通用户创建的表)

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建不同权限用户; expect:成功
drop user if exists u_selectprivilege_0017_01;
drop user if exists u_selectprivilege_0017_02;
create user u_selectprivilege_0017_01 password 'test@123';
create user u_selectprivilege_0017_02 sysadmin password 'test@123';

--step3: 赋权给普通用户; expect:成功
grant create on schema public to u_selectprivilege_0017_01;

--step4: 切换普通用户创建表并向表中插入数据; expect:成功
set role u_selectprivilege_0017_01 password 'test@123';
select current_user;
create  table  public.t_selectprivilege_0017(id int primary key,name varchar(100));
insert into public.t_selectprivilege_0017 values(1,'beijing'),(2,'shanghai');

--step5: 切换超级sysadmin权限用户查询普通表; expect:查询结果为前面插入的两条数据
set role u_selectprivilege_0017_02 password 'test@123';
select current_user;
select * from  public.t_selectprivilege_0017;

--step6: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step7: 清理环境; expect:环境清理成功
drop table public.t_selectprivilege_0017 cascade;
drop user u_selectprivilege_0017_01 cascade;
drop user u_selectprivilege_0017_02  cascade;