-- @testpoint: 三权分立关闭时验证用户对于public模式下的视图没有select权限，赋予select权限之后可以查询,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建不同权限用户; expect:成功
drop user if exists u_selectprivilege_0030_01;
drop user if exists u_selectprivilege_0030_02;
create user u_selectprivilege_0030_01 createrole password 'test@130';
create user u_selectprivilege_0030_02 password 'test@130';

--step3: 赋权给createrole用户; expect:成功
grant create on schema public to u_selectprivilege_0030_01;

--step4: 切换createrole用户创建表，视图并向表中插入数据; expect:成功
set role u_selectprivilege_0030_01 password 'test@130';
select current_user;
create table public.t_selectprivilege_0030(id int,name varchar(100));
insert into public.t_selectprivilege_0030 values(1,'beijing'),(2,'shanghai');
create or replace view public.v_selectprivilege_0030 as select * from public.t_selectprivilege_0030;

--step5: 切换普通用户select视图; expect:权限拒绝
set role u_selectprivilege_0030_02 password 'test@130';
select current_user;
select * from  public.v_selectprivilege_0030;

--step6: 切换createrole用户授权; expect:成功
set role u_selectprivilege_0030_01 password 'test@130';
select current_user;
grant select on table public.v_selectprivilege_0030 to u_selectprivilege_0030_02;

--step7: 切换select视图; expect:查询结果为前面插入的两条数据
set role u_selectprivilege_0030_02 password 'test@130';
select current_user;
select * from  public.v_selectprivilege_0030;

--step8: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step9: 清理环境; expect:环境清理成功
drop view public.v_selectprivilege_0030 cascade;
drop table public.t_selectprivilege_0030 cascade;
drop user u_selectprivilege_0030_01 cascade;
drop user u_selectprivilege_0030_02  cascade;