-- @testpoint: array_agg函数union all/union/minus
drop table if exists t_varray_array_agg;
create table t_varray_array_agg
(
f1 integer,
f2 integer,
f3 varchar(30)
);
insert into t_varray_array_agg values (1,100,'fdfd1'), (1,100,'fdfd'), (2,200,'fdfd'), (2, 220,'fdfd'), (3,300,'fdfd'), (4, 300,'fdfd'), (4, 500,'fdfd'), (5,600,'fdfd');
commit;
SELECT array_agg(f3) FROM t_varray_array_agg GROUP BY f1 union SELECT array_agg(f3) FROM t_varray_array_agg GROUP BY f1;
SELECT array_agg(f3) FROM t_varray_array_agg GROUP BY f1 union all SELECT array_agg(f3) FROM t_varray_array_agg GROUP BY f1;
SELECT array_agg(f3) FROM t_varray_array_agg GROUP BY f1 minus SELECT array_agg(f3) FROM t_varray_array_agg GROUP BY f1;
drop table if exists t_varray_array_agg;