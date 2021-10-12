-- @testpoint: hll_add_agg(hll_hashval, int32 log2m, int32 regwidth, int64 expthresh),把哈希后的数据按照分组放到hll中, 依次指定参数log2m、regwidth、expthresh

create table t_id(id int);
insert into t_id values(generate_series(1,10));
select  hll_add_agg(hll_hash_text(id), 10, 1, -1) from t_id ;
drop table t_id;

select hll_add_agg(hll_hash_boolean(true), 16, 5, 7);
select hll_add_agg (hll_hash_smallint(32767, 0), null, null, null);
