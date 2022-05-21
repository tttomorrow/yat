-- @testpoint: 三权分立关闭时验证用户对于私有模式下的视图没有select权限,赋予select权限之后可以查询表,合理报错

--step1: 查询三权分立参数enableSeparationOfDuty; expect:显示默认值off
show enableSeparationOfDuty;

--step2: 创建用户; expect:成功
drop user if exists u_selectprivilege_0027;
drop user if exists u_selectprivilege_0027_1;
create user u_selectprivilege_0027   password 'test@123';
create user u_selectprivilege_0027_1   password 'test@123';

--step3: 切换用户1创建表\视图\表中插入数据并将schema访问权限赋予用户2; expect:成功
set role u_selectprivilege_0027 password 'test@123';
select current_user;
create table t_selectprivilege_0027(id int,name varchar(100));
insert into t_selectprivilege_0027 values(1,'beijing'),(2,'shanghai');
create or replace view v_selectprivilege_0027 as select * from t_selectprivilege_0027;
grant usage on schema u_selectprivilege_0027 to u_selectprivilege_0027_1;

--step4: 切换用户2查询视图; expect:合理报错
reset role;
set role u_selectprivilege_0027_1 password 'test@123';
select current_user;
select * from  u_selectprivilege_0027.v_selectprivilege_0027;

--step5: 切换用户1授权; expect:成功
reset role;
set role u_selectprivilege_0027 password 'test@123';
select current_user;
grant select on table v_selectprivilege_0027 to u_selectprivilege_0027_1;

--step6: 切换用户2查询视图; expect:成功
reset role;
set role u_selectprivilege_0027_1 password 'test@123';
select current_user;
select * from  u_selectprivilege_0027.v_selectprivilege_0027;

--step7: 重置当前用户; expect:重置成功
reset role;
select current_user;

--step8: 清理环境; expect:环境清理成功
drop view u_selectprivilege_0027.v_selectprivilege_0027;
drop table u_selectprivilege_0027.t_selectprivilege_0027;
drop user u_selectprivilege_0027 cascade;
drop user u_selectprivilege_0027_1 cascade;