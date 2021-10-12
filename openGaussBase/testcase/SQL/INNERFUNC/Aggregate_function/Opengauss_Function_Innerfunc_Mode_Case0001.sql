-- @testpoint: 函数mode() within group (order by value anyelement),返回某列中出现频率最高的值，如果多个值频率相同，则返回最小的那个值

select mode() within group (order by value) from (values(1, 'a'), (2, 'b'), (2, 'c')) as aa(value, bb);
select mode() within group (order by tag) from (values(1, 'a'), (2, 'b'), (2, 'c')) as v(value, tag);
select mode() within group (order by tag) from (values(1, 'a'), (2, 'b'), (2, 'c')) as v(tag);