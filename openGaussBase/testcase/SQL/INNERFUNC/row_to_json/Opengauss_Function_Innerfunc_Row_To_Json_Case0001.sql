-- @testpoint: row_to_json函数返回JSON类型的行
select row_to_json(row(1,'foo',2)) from sys_dummy;
select row_to_json(row(1)) from sys_dummy;
select row_to_json(row(2.222)) from sys_dummy;
select row_to_json(row('three')) from sys_dummy;
select row_to_json(row(true)) from sys_dummy;
select row_to_json(row(interval '3' day)) from sys_dummy;
select row_to_json(row(to_date('2020-06-16'))) from sys_dummy;
select row_to_json(row(inet('10.183.187.233'))) from sys_dummy;
select row_to_json(row((3, 3))) from sys_dummy;
select row_to_json(row(B'101')) from sys_dummy;
select row_to_json(row('The Fat Rats'::tsvector)) from sys_dummy;
select row_to_json(row('52093.89'::money::numeric::float8)) from sys_dummy;