-- @testpoint: opengauss比较操作符<=，参数互换结果互斥
-- 运算的交换性
select 'students'::text <= 'student'::text;
select 'student'::text <= 'student'::text;
select '521'::money <= '520'::money;
select '520'::money <= '521'::money;
select 't'::BOOLEAN <= 'f'::BOOLEAN;
select 'f'::BOOLEAN <= 't'::BOOLEAN;