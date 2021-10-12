-- @testpoint: 存储过程for loop 语句使用

drop table if exists t_user;

create table t_user(
  month_id varchar2(20),
  user_id int,
  name varchar2(200),
  sal number
);

insert into t_user values('201701',1,'xq',1200);
insert into t_user values('201702',1,'xq',1260);
insert into t_user values('201702',1,'xq',1323);
insert into t_user values('201702',1,'xq',1389.15);
insert into t_user values('201703',1,'xq',1458.61);
insert into t_user values('201704',1,'xq',1531.54);
insert into t_user values('201705',1,'xq',1608.12);
insert into t_user values('201706',1,'xq',1688.53);
insert into t_user values('201707',1,'xq',1772.96);
insert into t_user values('201708',1,'xq',1861.61);
insert into t_user values('201709',1,'xq',1954.69);
insert into t_user values('201710',1,'xq',2052.42);
insert into t_user values('201711',1,'xq',2155.04);
insert into t_user values('201712',1,'xq',2262.79);
insert into t_user values('201801',1,'xq',2375.93);
insert into t_user values('201802',1,'xq',2494.73);
insert into t_user values('201803',1,'xq',2619.47);
insert into t_user values('201703',2,'ll',1200);
insert into t_user values('201704',2,'ll',1260);
insert into t_user values('201704',2,'ll',1323);
insert into t_user values('201704',2,'ll',1389.15);
insert into t_user values('201705',2,'ll',1458.61);
insert into t_user values('201706',2,'ll',1531.54);
insert into t_user values('201707',2,'ll',1608.12);
insert into t_user values('201805',2,'ll',1688.53);
insert into t_user values('201806',2,'ll',1772.96);
insert into t_user values('201807',2,'ll',1861.61);
insert into t_user values('201808',2,'ll',1954.69);
insert into t_user values('201809',2,'ll',2052.42);

create or replace procedure p005(v_id int) is
begin
  for i in (select month_id,
                   user_id,
                   sal,
                   sum(sal) over(partition by t.user_id order by month_id, sal desc,name) total_sal
              from t_user t
             where month_id >= '201001'
               and user_id = v_id
             order by user_id, month_id, sal desc,total_sal,name) 
			 loop
  end loop;
  raise notice '###################################################';
  for i in (select t.month_id,
                   t.user_id,
                   t.sal,                  
                   (select sum(sal)
                      from (select month_id, user_id, sal
                              from t_user t
                             where user_id = v_id
                             order by month_id, sal desc) t1
                     ) total_sal
              from (select t.*
                      from (select month_id, user_id, sal
                              from t_user t
                             where user_id = v_id
                             order by month_id, sal desc) t) t
             order by month_id, sal desc,user_id,total_sal) 
			 loop
  end loop;
end;
/

call p005(1);
call p005(2);
drop procedure p005;
drop table t_user;


