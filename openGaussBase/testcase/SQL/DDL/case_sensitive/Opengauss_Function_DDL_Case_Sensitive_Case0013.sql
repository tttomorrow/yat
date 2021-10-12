--  @testpoint: --WITH语句验证表名大小写
with
t1 as (select * from false_1)
select * from t1;
with
t1 as (select * from FALSE_1)
SELECT * FROM t1;