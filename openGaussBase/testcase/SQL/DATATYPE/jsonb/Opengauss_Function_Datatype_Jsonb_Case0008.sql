-- @testpoint: jsonb格式校验：Num-jsonb（不符合格式合理报错）

--符合格式
--1.正负数
select '100'::jsonb;
select '-99'::jsonb;
--2.小数
select '0.99'::jsonb;
select '99.99'::jsonb;
select '-0.98'::jsonb;
--3.0
select '0'::jsonb;
--4.科学计数法
select '-1.5e-5'::jsonb;
--不符合格式
--1.不支持多余的前导零
select '007'::jsonb;
select '00.7'::jsonb;
--2.正数最前面不支持加 +
select '+100'::jsonb;
select '+00.7'::jsonb;
--3.不支持NaN
select 'NaN'::jsonb;
--4.不支持infinity
select 'infinity'::jsonb;