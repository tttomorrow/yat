-- @testpoint: array_agg函数在case when中使用
drop table if exists t_varray_array_agg;
create table t_varray_array_agg
(
f1 integer,
f2 integer,
f3 varchar(30)
);
insert into t_varray_array_agg values (1,100,'fdfd1'), (1,100,'fdfd'), (2,200,'fdfd'), (2, 220,'fdfd'), (3,300,'fdfd'), (4, 300,'fdfd'), (4, 500,'fdfd'), (5,600,'fdfd');
commit;
SELECT case when array_agg(f3)='{fdfd,fdfd}' then '1' else '0' end FROM t_varray_array_agg GROUP BY f1 order by f1;
SELECT case when 1=1 then array_agg(f3)='{fdfd,fdfd}' else '0' end FROM t_varray_array_agg GROUP BY f1 order by f1;
SELECT case when 1=0 then '1' else array_agg(f3)='{fdfd,fdfd}' end FROM t_varray_array_agg GROUP BY f1 order by f1;
drop table if exists t_varray_array_agg;