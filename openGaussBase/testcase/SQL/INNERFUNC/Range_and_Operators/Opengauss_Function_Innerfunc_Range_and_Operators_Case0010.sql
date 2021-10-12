-- @testpoint: lower_inc(anyrange) 描述：是否包含下界，如参为无效参数时，合理报错

select lower_inc(macaddr('08:00:2b:01:02:03'::macaddr ,'08:00:2b:01:02:03'::macaddr)) as result;
create type bugstatus as enum ('create', 'modify', 'closed');
drop type bugstatus;
select lower_inc(bugstatus (create, closed)) as result;
select lower_inc(uuid('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid,'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22'::uuid)) as result;