-- @testpoint: 参数为表达式
select nullif((0.12+1)*1.2,1.344);
select nullif(1>2,2=2);
select nullif(abs(-0.9),0.9);