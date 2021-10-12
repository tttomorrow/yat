-- @testpoint: hll_add_agg(hll_hashval, int32 log2m, int32 regwidth, int64 expthresh),入参为其他类型时，合理报错

create table t_id(id int);
insert into t_id values(generate_series(1,10));
select  hll_add_agg(hll_hash_text(id), 10, 1, -2) from t_id ;
drop table t_id;

select hll_add_agg(hll_hash_boolean(true), 16, 5, 8);
select hll_add_agg (hll_hash_smallint(32767, 0), null, 6, null);