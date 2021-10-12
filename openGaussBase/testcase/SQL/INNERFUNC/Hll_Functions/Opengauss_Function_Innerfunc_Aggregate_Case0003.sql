-- @testpoint: hll_add_agg(hll_hashval, int32 log2m),把哈希后的数据按照分组放到hll中。 并指定参数log2m，取值范围是10到16

create table t_id(id int);
insert into t_id values(generate_series(1,10));
select  hll_add_agg(hll_hash_text(id), 10) from t_id ;
drop table t_id;

select hll_add_agg(hll_hash_boolean(true), 10);
select hll_add_agg (hll_hash_smallint(32767, 0), 16);
select hll_add_agg (hll_hash_smallint(32767, 0), null);