-- @testpoint:单独带一个存在的表查询该表的字段
drop index if exists idx;
create index idx on hint1_index_00000(id)local;
explain select /*+FULL(hint1_index_00000)*/ count(*) from hint1_index_00000 t1 right join hint1_index_00000 t2 on t1.id=t2.id
full outer join hint1_index_00000 t3 on t1.id=t3.id
right join hint1_index_00000 t4 on t1.id=t4.id
left join hint1_index_00000 t5 on t1.id=t5.id
inner join hint1_index_00000 t6 on t1.id=t6.id
left join hint1_index_00000 t7 on t1.id=t7.id
right join hint1_index_00000 t8 on t1.id=t8.id
right join hint1_index_00000 t9 on t1.id=t9.id
right join hint1_index_00000 t10 on t1.id=t10.id
full outer join hint1_index_00000 t11 on t1.id=t11.id;

drop index if exists idx;
create index idx on hint1_index_00000(id)local;
explain select count(*) from hint1_index_00000 t1 right join hint1_index_00000 t2 on t1.id=t2.id
full outer join hint1_index_00000 t3 on t1.id=t3.id
right join hint1_index_00000 t4 on t1.id=t4.id
left join hint1_index_00000 t5 on t1.id=t5.id
inner join hint1_index_00000 t6 on t1.id=t6.id
left join hint1_index_00000 t7 on t1.id=t7.id
right join hint1_index_00000 t8 on t1.id=t8.id
right join hint1_index_00000 t9 on t1.id=t9.id
right join hint1_index_00000 t10 on t1.id=t10.id
full outer join hint1_index_00000 t11 on t1.id=t11.id;
