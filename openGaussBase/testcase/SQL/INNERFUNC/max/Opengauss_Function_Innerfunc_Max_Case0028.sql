-- @testpoint: 函数调用max结合group by--inet

--step1:创建表; expect:成功
drop table if exists t_max_case0028;
create table t_max_case0028(id int, i inet);

--step2:创建函数; expect:成功
create or replace function f_max_case0028_inet()
returns table(r_i int, i_c inet)
as $$
begin
return query select id, max(i)  from t_max_case0028 group by id order by id;
end;
$$language plpgsql;/

--step3:调用函数; expect:空
select f_max_case0028_inet();

--step4:插入空值; expect:空 ::
insert into t_max_case0028 values(1, NULL);
select f_max_case0028_inet();
insert into t_max_case0028 values(1, '::');
select f_max_case0028_inet();

--step5:插入数据; expect:(1,::ffff) (2,::255.255.0.0/120)
insert into t_max_case0028 values(1, '::ffff/128'),(2, '::ffff:0/120');
select f_max_case0028_inet();

--tearDown
drop function f_max_case0028_inet;
drop table if exists t_max_case0028;

