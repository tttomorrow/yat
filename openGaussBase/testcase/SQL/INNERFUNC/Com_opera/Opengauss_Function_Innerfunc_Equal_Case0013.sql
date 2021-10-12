-- @testpoint: opengauss比较操作符,参数互换结果互斥

-- 运算的交换性
select 'ABC'::text = 'ABC'::CHAR(3);
select 'ABC'::CHAR(3) = 'ABC'::text;
select '521'::money = '520'::money;
select '520'::money = '521'::money;
select 't'::BOOLEAN = 'TRUE'::BOOLEAN;
select 'TRUE'::BOOLEAN = 't'::BOOLEAN;