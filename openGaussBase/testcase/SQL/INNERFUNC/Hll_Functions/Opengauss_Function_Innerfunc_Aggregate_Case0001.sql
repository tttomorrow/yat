-- @testpoint: hll_add_agg(hll_hashval) 描述：把哈希后的数据按照分组放到hll中

create table t_id(id int);
insert into t_id values(generate_series(1,10));
select  hll_add_agg(hll_hash_text(id)) from t_id ;
drop table t_id;

select hll_add_agg(hll_hash_boolean(true));
select hll_add_agg (hll_hash_smallint(32767, 0));

