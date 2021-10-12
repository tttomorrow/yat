-- @testpoint: json格式校验：Num-json（不符合格式合理报错）

--符合格式
--1.正负数
select '100'::json;
select '-99'::json;
--2.小数
select '0.99'::json;
select '99.99'::json;
select '-0.98'::json;
--3.0
select '0'::json;
--4.科学计数法
select '-1.5e-5'::json;
--不符合格式
--1.不支持多余的前导零
select '007'::json;
select '00.7'::json;
--2.正数最前面不支持加 +
select '+100'::json;
select '+00.7'::json;
--3.不支持NaN
select 'NaN'::json;
--4.不支持infinity
select 'infinity'::json;