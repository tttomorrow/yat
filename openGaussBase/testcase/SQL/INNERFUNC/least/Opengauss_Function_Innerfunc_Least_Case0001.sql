-- @testpoint: union all/union的测试
select least('14541.2353212','5412121.23211454541','sdsdsdaffdfsfdfdff') from sys_dummy union all select least('14541.2353212','大幅度发多少','sdsdsdaffdfsfdfdff')from sys_dummy;
select case when 2>1 then least('14541.2353212','5412121.23211454541','sdsdsdaffdfsfdfdff') else '0' end from sys_dummy
union
select case when 2>232 then '3432' else least('14541.2353212','大幅度发多少','sdsdsdaffdfsfdfdff') end from sys_dummy;