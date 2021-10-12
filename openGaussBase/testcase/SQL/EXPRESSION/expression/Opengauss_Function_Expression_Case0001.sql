--  @testpoint: 逻辑表达式：覆盖基本逻辑操作符

--TRUE AND FALSE
select 1<2 and 'a' > 'b' as result;

--TRUE AND TRUE
select 1<2 and 'a' < 'b' as result;

--TRUE AND NULL
select 1<2 and NULL as result;
select (1<2) & (NULL) as result;

--FALSE AND NULL
select 1>2 and NULL as result;

--TRUE AND FALSE
select 1>2 and  'a' > 'b'  as result;

--NULL AND NULL
select NULL and NULL as result;

--TRUE OR FALSE
select 1<2 or 'a' > 'b' as result;

--TRUE OR NULL
select 1<2 or NULL as result;

--FALSE OR NULL
select 1>2 or NULL as result;

--NULL OR NULL
select NULL or NULL as result;

--NOT TRUE
select not 1<2 as result;

--NOT NULL
select not NULL as result;

--NOT FALSE
select not 1>2 as result;

--优先级 NOT>AND>OR
select 1>2 and not 1>2 or 1>2 as result;
select not 1>2 and 1>2 or 1>2 as result;
select 1>2 or 1>2 and not 1>2 as result;

select not 1<2 and 1<2 or 1<2 as result;
select  1<2 and not 1<2 or 1<2 as result;
select  1<2 or 1<2 and not 1<2 as result;

select not 1>2 and 1<2 or 1<2 as result;
select  1<2 and not 1>2 or 1<2 as result;
select  1<2 or 1<2 and not 1>2 as result;

--清理环境
--no need to clean
