-- @testpoint: 查询系统表，校验列存cbtree是否支持唯一索引

select amcanunique from pg_am where amname='cbtree';
