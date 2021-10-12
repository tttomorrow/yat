--  @testpoint: --WITH语句验证字段名大小写
with
t1 as (select b from false_1)
select * from t1;
with
t1 as (select B from false_1)
select * from t1;