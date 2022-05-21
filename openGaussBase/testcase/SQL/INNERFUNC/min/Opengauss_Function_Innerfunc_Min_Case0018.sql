-- @testpoint: 函数调用min结合group by--cidr

--step1:创建表; expect:成功
drop table if exists t_min_case0018;
create table t_min_case0018(id int, i cidr);

--step2:创建函数; expect:成功
create or replace function f_min_case0018(out min_id int, out min_c cidr)
returns setof record
as $$
begin
return query select id as min_id, min(i)::cidr as min_c from t_min_case0018 group by id order by id;
end;
$$language plpgsql;/

--step3:调用函数; expect:空
select f_min_case0018();

--step4:插入空值; expect:空 ::
insert into t_min_case0018 values(1, NULL);
select f_min_case0018();
insert into t_min_case0018 values(1, '::');
select f_min_case0018();

--step5:插入数据; expect:(1,::) (2,::255.255.0.0/120)
insert into t_min_case0018 values(1, '::ffff/128'),(2, '::ffff:0/120');
select f_min_case0018();

--tearDown
drop function f_min_case0018;
drop table if exists t_min_case0018;

