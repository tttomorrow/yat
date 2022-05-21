-- @testpoint: 函数median(expression) [over (query partition clause)]，求取中位数，入参为有效值

select median(name) from (values(1), (5), (3), (4)) as tt(name);
select median(id) from (values(1), (156.2), (3), (4)) as test(id);
select median(id) from (values(1156562655), (1564896295), (3262645265), (44848626595)) as test(id);
select median(days) from (values(interval '4' day), (interval '5' day), (interval '6' day), (interval '7' day)) as test(days);
select median(id) from (values('151'), ('156.2'), ('593'), ('464')) as test(id);