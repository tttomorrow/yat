--  @testpoint:opengauss关键字true(保留)，作为逻辑操作符，验证功能正常


select true and false as result;
select false and true as result;

select true or false as result;
select false or true as result;

select true and null as result;
select true or null as result;

select not true as result;

