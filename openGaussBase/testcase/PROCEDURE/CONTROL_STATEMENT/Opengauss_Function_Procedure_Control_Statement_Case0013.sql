-- @testpoint: 存储过程loop语句

drop table if exists t_user;
create table t_user(
  user_id int,
  name varchar2(200),
  sal number
);

insert into t_user values(1,'xq',1200);
insert into t_user values(2,'ll',900.0);
insert into t_user values(3,'wwj',1000);
insert into t_user values(1,'xq',899.999);
insert into t_user values(4,'ly',899.9990);

select * from t_user order by user_id;

create or replace procedure pro1(v_id int) is
begin
  for i in (select user_id, sum(sal) sal
		from t_user t where t.user_id <= v_id group by user_id having sum(sal) > 1order by user_id) 
  loop
    insert into t_user values (i.user_id, '总工资', i.sal);
    update t_user t set t.sal = round(t.sal * 0.99,2) where name = '总工资' and user_id=i.user_id;
    delete from t_user where name <> '总工资' and user_id <= v_id;
  end loop;
end;
/

call pro1(3);
select * from t_user order by user_id;
call pro1(4);
select * from t_user order by user_id;

drop table t_user;
drop procedure pro1;



