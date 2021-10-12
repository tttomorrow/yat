-- @testpoint: opengauss比较操作符>=，交换后结果互斥性
-- 运算的交换性
select 'students'::text >= 'abc'::text;
select 'abc'::text >= 'students'::text;
select '521'::money >= '520'::money;
select '520'::money >= '521'::money;
select 't'::BOOLEAN >= 'f'::BOOLEAN;
select 'f'::BOOLEAN >= 't'::BOOLEAN;