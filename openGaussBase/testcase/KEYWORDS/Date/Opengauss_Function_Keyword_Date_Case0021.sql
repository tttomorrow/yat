-- @testpoint: opengauss关键字date(非保留)，作为函数名，部分测试点合理报错

--关键字不带引号-失败（不可以是函数名）
drop function if exists date;
create function date(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带双引号-成功（开发者指南备注不能是函数，实际加引号作为函数名成功了，引号的作用是什么，需要与开发确认）
drop function if exists "date"(i integer);
create function "date"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
select "date"(3);
drop function if exists "date"(i integer);
--关键字带单引号-合理报错
drop function if exists 'date';
create function 'date'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `date`;
create function `date`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/