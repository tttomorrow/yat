-- @testpoint: 三权分立关闭时验证用户对于public模式下的分区表没有select权限，赋予select权限之后可以查询表,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建不同权限用户; expect:成功
drop user if exists u_selectprivilege_0028_01;
drop user if exists u_selectprivilege_0028_02;
create user u_selectprivilege_0028_01 createrole password 'test@128';
create user u_selectprivilege_0028_02 password 'test@128';

--step3: 赋权给createrole用户; expect:成功
grant create on schema public to u_selectprivilege_0028_01;

--step4: 切换createrole用户创建分区表并向表中插入数据; expect:成功
set role u_selectprivilege_0028_01 password 'test@128';
select current_user;
create table public.t_selectprivilege_0028(id int,name varchar(100))
partition by range(id)
(partition p1 values less than(10),
partition p2 values less than(20),
partition p3 values less than(30),
partition pmax values less than(maxvalue));
insert into public.t_selectprivilege_0028 values(1,'beijing'),(2,'shanghai');

--step5: 切换普通用户查询表; expect:权限拒绝
set role u_selectprivilege_0028_02 password 'test@128';
select current_user;
select * from  public.t_selectprivilege_0028;

--step5: 切换createrole用户授权; expect:成功
set role u_selectprivilege_0028_01 password 'test@128';
select current_user;
grant select on table public.t_selectprivilege_0028 to u_selectprivilege_0028_02;

--step6: 切换普通用户2查询表; expect:查询结果为前面插入的两条数据
set role u_selectprivilege_0028_02 password 'test@128';
select current_user;
select * from  public.t_selectprivilege_0028;

--step7: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step8: 清理环境; expect:环境清理成功
drop table public.t_selectprivilege_0028 cascade;
drop user u_selectprivilege_0028_01 cascade;
drop user u_selectprivilege_0028_02  cascade;