--  @testpoint: 其他数据类型的支持,字符型0 1和数字型0 1

--TRUE AND FALSE
select 1 and 0 as result;
select '1' and '0' as result;
select 'on' and 'off' as result;

--TRUE AND TRUE
select 1 and 1 as result;
select '1' and '1' as result;
select 'y' and 'y' as result;

--TRUE AND NULL
select 1 and NULL as result;
select '1' and NULL as result;
select 'y' and NULL as result;

--FALSE AND NULL
select 0 and NULL as result;
select '0' and NULL as result;
select 'n' and NULL as result;

--TRUE AND FALSE
select 0 and  0  as result;

--TRUE OR FALSE
select 1 or 0 as result;
select '1' or '0' as result;

--TRUE OR NULL
select 1 or NULL as result;
select '1' or NULL as result;

--FALSE OR NULL
select 0 or NULL as result;
select '0' or NULL as result;

--NOT TRUE
select not 1 as result;
select not '1' as result;

--NOT FALSE
select not '0' as result;

--优先级 NOT>AND>OR
select 0 and not 0 or 0 as result;
select not 0 and 0 or 0 as result;
select 0 or 0 and not 0 as result;

select not 1 and 1 or 1 as result;
select  1 and not 1 or 1 as result;
select  1 or 1 and not 1 as result;

select not 0 and 1 or 1 as result;
select  1 and not 0 or 1 as result;
select  1 or 1 and not 0 as result;

select '0' and not '0' or '0' as result;
select not '0' and '0' or '0' as result;
select '0' or '0' and not '0' as result;

select not '1' and '1' or '1' as result;
select  '1' and not '1' or '1' as result;
select  '1' or '1' and not '1' as result;

select not '0' and '1' or '1' as result;
select  '1' and not '0' or '1' as result;
select  '1' or '1' and not '0' as result;

--清理环境
--no need to clean
