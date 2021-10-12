-- @testpoint: upper_inf(anyrange) 描述：上界是否为无穷，入参为无效值时，合理报错

select lower_inf(macaddr('08:00:2b:01:02:03'::macaddr ,'08:00:2b:01:02:03'::macaddr)) as result;
create type bugstatus as enum ('create', 'modify', 'closed');
drop type bugstatus;
select lower_inf(bugstatus '(create, )') as result;
select lower_inf(uuid('(a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11,a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22)'::uuid)) as result;

