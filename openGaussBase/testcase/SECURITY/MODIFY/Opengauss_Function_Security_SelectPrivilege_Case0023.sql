-- @testpoint: 三权分立关闭时验证普通用户对于public模式下的表没有select权限，赋予select权限之后可以查询表,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建两个普通用户; expect:成功
drop user if exists u_selectprivilege_0023_01;
drop user if exists u_selectprivilege_0023_02;
create user u_selectprivilege_0023_01 password 'test@123';
create user u_selectprivilege_0023_02 password 'test@123';

--step3: 赋权给普通用户1; expect:成功
grant create on schema public to u_selectprivilege_0023_01;

--step4: 切换普通用户1创建表并向表中插入数据; expect:成功
set role u_selectprivilege_0023_01 password 'test@123';
select current_user;
create table public.t_selectprivilege_0023(id int,name varchar(100));
insert into public.t_selectprivilege_0023 values(1,'beijing'),(2,'shanghai');

--step5: 切换普通用户2查询表; expect:权限拒绝
set role u_selectprivilege_0023_02 password 'test@123';
select current_user;
select * from  public.t_selectprivilege_0023;

--step6: 切换普通用户1授权; expect:成功
set role u_selectprivilege_0023_01 password 'test@123';
select current_user;
grant select on table public.t_selectprivilege_0023 to u_selectprivilege_0023_02;

--step7: 切换普通用户2查询表; expect:查询结果为前面插入的两条数据
set role u_selectprivilege_0023_02 password 'test@123';
select current_user;
select * from  public.t_selectprivilege_0023;

--step8: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step9: 清理环境; expect:环境清理成功
drop table public.t_selectprivilege_0023 cascade;
drop user u_selectprivilege_0023_01 cascade;
drop user u_selectprivilege_0023_02  cascade;