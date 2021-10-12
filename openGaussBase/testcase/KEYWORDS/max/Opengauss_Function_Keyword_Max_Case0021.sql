--  @testpoint:opengauss关键字max(非保留)，作为函数名

--关键字不带引号-成功

create function max(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function max (i integer);
--关键字带双引号-成功

create function "max"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function "max" (i integer);
--关键字带单引号-合理报错

create function 'max'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function 'max'(i integer);
--关键字带反引号-合理报错

create function `max`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function  `max`(i integer);
