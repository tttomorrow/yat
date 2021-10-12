-- @testpoint: 进行分词时，顺序进行，去除重复

select 'fat & rat'::tsquery;
select 'fat & (rat | cat)'::tsquery;
select 'fat & rat & ! cat'::tsquery;