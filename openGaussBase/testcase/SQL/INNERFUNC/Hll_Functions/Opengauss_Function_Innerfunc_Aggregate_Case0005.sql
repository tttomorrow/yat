-- @testpoint: hll_add_agg(hll_hashval,int32 log2m,int32 regwidth),把哈希后的数据按照分组放到hll中。依次制定参数log2m，regwidth。regwidth取值范围是1到5

create table t_id(id int);
insert into t_id values(generate_series(1,10));
select  hll_add_agg(hll_hash_text(id), 10, 1) from t_id ;
drop table t_id;

select hll_add_agg(hll_hash_boolean(true), 16, 5);
select hll_add_agg (hll_hash_smallint(32767, 0), null, null);
